import os
import json
import tarfile
import tempfile
import re
import shutil
from typing import Dict, Any, List, Tuple

from audit import calculate_entropy

SUSPICIOUS_TOKENS = [
    r'\beval\s*\(',
    r'\bFunction\s*\(',
    r'\bchild_process\b',
    r'\bcurl\s+',
    r'\bwget\s+',
    r'\bnc\s+',
    r'\brequire\s*\(\s*[\'"]child_process[\'"]\s*\)',
    r'\bexec\s*\(',
    r'\bspawn\s*\(',
    r'\bexecSync\s*\(',
    r'\bspawnSync\s*\(',
    r'https?://[^\s\'"]+',
    r'\bfetch\s*\(',
    r'\.send\s*\(',
    r'XMLHttpRequest',
    r'WebSocket',
]

INSTALL_SCRIPTS = ["postinstall", "preinstall", "install", "prepare", "prepublish"]


def scan_tarball(tarball_path: str) -> Dict[str, Any]:
    findings = {
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
    
    if not os.path.exists(tarball_path):
        return findings
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            safe_members = []
            for member in tar.getmembers():
                if member.name.startswith('/') or '..' in member.name:
                    continue
                safe_members.append(member)
            tar.extractall(temp_dir, members=safe_members)
        
        package_json_path = None
        for root, dirs, files in os.walk(temp_dir):
            if "package.json" in files:
                package_json_path = os.path.join(root, "package.json")
                break
        
        if package_json_path:
            try:
                with open(package_json_path, "r", encoding="utf-8", errors="ignore") as f:
                    pkg_data = json.load(f)
                    scripts = pkg_data.get("scripts", {})
                    
                    for script_name in INSTALL_SCRIPTS:
                        if script_name in scripts:
                            findings["has_postinstall"] = True
                            script_content = scripts[script_name]
                            findings["install_scripts"].append({
                                "name": script_name,
                                "content": script_content[:500]
                            })
                            
                            if any(cmd in script_content.lower() for cmd in ["curl", "wget", "nc ", "bash", "sh "]):
                                findings["has_network_commands"] = True
                                findings["network_patterns"].append({
                                    "file": "package.json",
                                    "script": script_name,
                                    "snippet": script_content[:200]
                                })
            except:
                pass
        
        for root, dirs, files in os.walk(temp_dir):
            for filename in files:
                if not filename.endswith(('.js', '.ts', '.mjs', '.cjs')):
                    continue
                
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, temp_dir)
                
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    scan_file_content(content, relative_path, findings)
                    
                except Exception as e:
                    continue
    
    except Exception as e:
        print(f"Error scanning tarball: {e}")
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return findings


def scan_file_content(content: str, file_path: str, findings: Dict[str, Any]):
    for pattern in SUSPICIOUS_TOKENS[:3]:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            if "eval" in pattern.lower() or "function" in pattern.lower():
                findings["has_eval_function"] = True
                snippet = extract_snippet(content, pattern)
                findings["eval_patterns"].append({
                    "file": file_path,
                    "pattern": pattern,
                    "snippet": snippet
                })
    
    for pattern in SUSPICIOUS_TOKENS[3:7]:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            findings["has_network_commands"] = True
            snippet = extract_snippet(content, pattern)
            findings["network_patterns"].append({
                "file": file_path,
                "pattern": pattern,
                "snippet": snippet
            })
    
    long_strings = re.findall(r'["\'][A-Za-z0-9+/=]{100,}["\']', content)
    for s in long_strings:
        entropy = calculate_entropy(s)
        if entropy > 4.0:
            findings["has_high_entropy"] = True
            findings["high_entropy_strings"].append({
                "file": file_path,
                "entropy": round(entropy, 2),
                "length": len(s),
                "snippet": s[:100] + "..." if len(s) > 100 else s
            })
    
    hex_patterns = re.findall(r'\\x[0-9a-fA-F]{2}(?:\\x[0-9a-fA-F]{2}){50,}', content)
    for h in hex_patterns:
        findings["has_high_entropy"] = True
        findings["high_entropy_strings"].append({
            "file": file_path,
            "type": "hex_encoded",
            "length": len(h),
            "snippet": h[:100] + "..." if len(h) > 100 else h
        })


def extract_snippet(content: str, pattern: str) -> str:
    match = re.search(pattern, content, re.IGNORECASE)
    if match:
        start = max(0, match.start() - 50)
        end = min(len(content), match.end() + 50)
        return content[start:end]
    return ""


def get_tarball_summary(findings: Dict[str, Any]) -> List[str]:
    summary = []
    
    if findings["has_postinstall"]:
        scripts = [s["name"] for s in findings["install_scripts"]]
        summary.append(f"Install scripts found: {', '.join(scripts)}")
    
    if findings["has_network_commands"]:
        summary.append(f"Network/shell commands detected in {len(findings['network_patterns'])} location(s)")
    
    if findings["has_eval_function"]:
        summary.append(f"eval()/Function() calls in {len(findings['eval_patterns'])} location(s)")
    
    if findings["has_high_entropy"]:
        summary.append(f"High-entropy strings in {len(findings['high_entropy_strings'])} location(s)")
    
    return summary
