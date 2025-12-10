import httpx
import json
import sqlite3
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

CACHE_DB = os.path.join(os.path.dirname(__file__), "cache.db")
CACHE_TTL_SECONDS = 24 * 60 * 60


def init_cache():
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registry_cache (
            package_name TEXT PRIMARY KEY,
            data TEXT,
            cached_at REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS report_cache (
            package_name TEXT PRIMARY KEY,
            report TEXT,
            cached_at REAL
        )
    """)
    conn.commit()
    conn.close()


def get_cached_registry(package_name: str) -> Optional[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT data, cached_at FROM registry_cache WHERE package_name = ?",
            (package_name,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            data, cached_at = row
            if time.time() - cached_at < CACHE_TTL_SECONDS:
                return json.loads(data)
    except:
        pass
    return None


def set_cached_registry(package_name: str, data: Dict[str, Any]):
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO registry_cache (package_name, data, cached_at) VALUES (?, ?, ?)",
            (package_name, json.dumps(data), time.time())
        )
        conn.commit()
        conn.close()
    except:
        pass


def get_cached_report(package_name: str) -> Optional[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT report, cached_at FROM report_cache WHERE package_name = ?",
            (package_name,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            report, cached_at = row
            if time.time() - cached_at < CACHE_TTL_SECONDS:
                return json.loads(report)
    except:
        pass
    return None


def set_cached_report(package_name: str, report: Dict[str, Any]):
    try:
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO report_cache (package_name, report, cached_at) VALUES (?, ?, ?)",
            (package_name, json.dumps(report), time.time())
        )
        conn.commit()
        conn.close()
    except:
        pass


async def fetch_package_metadata(package_name: str) -> Dict[str, Any]:
    init_cache()
    
    cached = get_cached_registry(package_name)
    if cached:
        return cached
    
    url = f"https://registry.npmjs.org/{package_name}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        
        if response.status_code == 404:
            return {"error": "Package not found", "status": 404}
        
        response.raise_for_status()
        data = response.json()
        
        set_cached_registry(package_name, data)
        return data


def extract_package_info(metadata: Dict[str, Any]) -> Dict[str, Any]:
    if "error" in metadata:
        return metadata
    
    latest_version = metadata.get("dist-tags", {}).get("latest", "unknown")
    versions = metadata.get("versions", {})
    time_data = metadata.get("time", {})
    maintainers = metadata.get("maintainers", [])
    
    latest_data = versions.get(latest_version, {})
    repository = latest_data.get("repository") or metadata.get("repository")
    dependencies = latest_data.get("dependencies", {})
    dev_dependencies = latest_data.get("devDependencies", {})
    dist = latest_data.get("dist", {})
    tarball_url = dist.get("tarball", "")
    scripts = latest_data.get("scripts", {})
    
    return {
        "name": metadata.get("name", ""),
        "latest_version": latest_version,
        "versions": list(versions.keys()),
        "time": time_data,
        "maintainers": maintainers,
        "repository": repository,
        "dependencies": dependencies,
        "dev_dependencies": dev_dependencies,
        "tarball_url": tarball_url,
        "scripts": scripts,
        "description": metadata.get("description", ""),
        "license": latest_data.get("license", "unknown"),
        "homepage": metadata.get("homepage", "")
    }


async def download_tarball(tarball_url: str, dest_path: str) -> bool:
    if not tarball_url:
        return False
    
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            response = await client.get(tarball_url)
            response.raise_for_status()
            
            with open(dest_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading tarball: {e}")
        return False
