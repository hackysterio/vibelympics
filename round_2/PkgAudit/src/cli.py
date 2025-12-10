#!/usr/bin/env python3
import sys
import os
import json
import asyncio

sys.path.insert(0, os.path.dirname(__file__))

from registry import fetch_package_metadata, extract_package_info, download_tarball, init_cache, set_cached_report
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
from datetime import datetime
import tempfile


async def audit_package(package_name: str) -> dict:
    init_cache()
    
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
    
    set_cached_report(package_name, report)
    
    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <package-name>", file=sys.stderr)
        print("Example: python cli.py express", file=sys.stderr)
        sys.exit(1)
    
    package_name = sys.argv[1].strip().lower()
    
    if not package_name:
        print("Error: Package name cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    report = asyncio.run(audit_package(package_name))
    
    if "error" in report:
        print(json.dumps({"error": report["error"]}, indent=2))
        sys.exit(1)
    
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
