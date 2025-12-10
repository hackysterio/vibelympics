import os
import sys
import json
import tempfile
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

sys.path.insert(0, os.path.dirname(__file__))

from registry import (
    fetch_package_metadata,
    extract_package_info,
    download_tarball,
    get_cached_report,
    set_cached_report,
    init_cache
)
from tarball_scanner import scan_tarball, get_tarball_summary
from audit import (
    find_typosquat_matches,
    calculate_publish_activity_score,
    calculate_maintainer_score,
    calculate_dependency_score,
    calculate_typosquat_score,
    calculate_tarball_score,
    calculate_final_risk_score,
    get_severity,
    generate_flags,
    parse_version_timeline,
    analyze_publish_activity,
    analyze_maintainers,
    analyze_dependencies,
    POPULAR_PACKAGES
)

app = FastAPI(
    title="PkgAudit",
    description="npm Package Ecosystem Auditor - Software Supply Chain Security Tool",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

init_cache()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/audit")
async def api_audit(pkg: str):
    if not pkg or not pkg.strip():
        raise HTTPException(status_code=400, detail="Package name is required")
    
    pkg = pkg.strip().lower()
    
    cached = get_cached_report(pkg)
    if cached:
        return JSONResponse(content=cached)
    
    report = await perform_audit(pkg)
    
    if "error" not in report:
        set_cached_report(pkg, report)
    
    return JSONResponse(content=report)


@app.post("/audit", response_class=HTMLResponse)
async def audit_form(request: Request, package: str = Form(...)):
    if not package or not package.strip():
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please enter a package name"
        })
    
    package = package.strip().lower()
    
    cached = get_cached_report(package)
    if cached:
        report = cached
    else:
        report = await perform_audit(package)
        if "error" not in report:
            set_cached_report(package, report)
    
    if "error" in report:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": report.get("error", "Unknown error occurred")
        })
    
    return templates.TemplateResponse("report.html", {
        "request": request,
        "report": report,
        "report_json": json.dumps(report, indent=2)
    })


@app.get("/api/report/{package}.json")
async def get_report(package: str):
    cached = get_cached_report(package.lower())
    if cached:
        return JSONResponse(content=cached)
    raise HTTPException(status_code=404, detail="Report not found in cache")


async def perform_audit(package_name: str) -> dict:
    try:
        metadata = await fetch_package_metadata(package_name)
        
        if "error" in metadata:
            return {"error": metadata.get("error", "Failed to fetch package")}
        
        pkg_info = extract_package_info(metadata)
        
        if "error" in pkg_info:
            return pkg_info
        
        publish_data = analyze_publish_activity(pkg_info.get("time", {}))
        maintainer_data = analyze_maintainers(
            pkg_info.get("maintainers", []),
            pkg_info.get("repository")
        )
        dependency_data = analyze_dependencies(pkg_info.get("dependencies", {}))
        
        min_distance, typosquat_matches = find_typosquat_matches(package_name)
        typosquat_data = {
            "min_distance": min_distance,
            "matches": typosquat_matches
        }
        
        tarball_findings = {
            "has_postinstall": False,
            "has_network_commands": False,
            "has_eval_function": False,
            "has_high_entropy": False,
            "install_scripts": [],
            "suspicious_files": [],
            "high_entropy_strings": [],
            "network_patterns": [],
            "eval_patterns": []
        }
        
        tarball_url = pkg_info.get("tarball_url", "")
        if tarball_url:
            with tempfile.NamedTemporaryFile(suffix=".tgz", delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                if await download_tarball(tarball_url, tmp_path):
                    tarball_findings = scan_tarball(tmp_path)
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        
        is_popular = package_name in POPULAR_PACKAGES
        
        publish_score = calculate_publish_activity_score(
            publish_data["releases_last_7d"],
            publish_data["releases_last_30d"],
            publish_data["is_dormant_then_sudden"],
            publish_data["latest_age_days"]
        )
        
        maintainer_score = calculate_maintainer_score(
            maintainer_data["count"],
            maintainer_data["has_recent_addition"],
            maintainer_data["has_github_repo"],
            maintainer_data["has_free_email"]
        )
        
        dependency_score = calculate_dependency_score(
            dependency_data["count"],
            dependency_data["deprecated_count"],
            dependency_data["missing_repo_count"]
        )
        
        typosquat_score = calculate_typosquat_score(min_distance, is_popular)
        
        tarball_score = calculate_tarball_score(
            tarball_findings["has_postinstall"],
            tarball_findings["has_network_commands"],
            tarball_findings["has_eval_function"],
            tarball_findings["has_high_entropy"]
        )
        
        final_score = calculate_final_risk_score(
            publish_score,
            maintainer_score,
            dependency_score,
            typosquat_score,
            tarball_score
        )
        
        severity = get_severity(final_score)
        
        flags = generate_flags(
            publish_data,
            maintainer_data,
            dependency_data,
            typosquat_data,
            tarball_findings
        )
        
        timeline = parse_version_timeline(pkg_info.get("time", {}))
        
        tarball_summary = get_tarball_summary(tarball_findings)
        
        report = {
            "package": package_name,
            "version": pkg_info.get("latest_version", "unknown"),
            "risk_score": final_score,
            "severity": severity,
            "risk_breakdown": {
                "publish_activity": publish_score,
                "maintainer": maintainer_score,
                "dependency": dependency_score,
                "typosquat": typosquat_score,
                "tarball_scan": tarball_score
            },
            "flags": flags,
            "evidence": {
                "maintainers": pkg_info.get("maintainers", []),
                "latest_release_date": publish_data.get("latest_release_date"),
                "tarball_findings": tarball_summary,
                "publish_timeline": timeline[:10],
                "repository": pkg_info.get("repository"),
                "dependencies_count": dependency_data["count"],
                "typosquat_matches": typosquat_matches,
                "description": pkg_info.get("description", ""),
                "license": pkg_info.get("license", "unknown"),
                "homepage": pkg_info.get("homepage", "")
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return report
        
    except Exception as e:
        return {"error": f"Audit failed: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
