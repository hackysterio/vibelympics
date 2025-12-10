import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

POPULAR_PACKAGES = [
    "react", "vue", "angular", "express", "lodash", "axios", "moment", "jquery",
    "webpack", "babel", "typescript", "eslint", "prettier", "jest", "mocha",
    "chai", "redux", "mobx", "next", "nuxt", "gatsby", "svelte", "ember",
    "backbone", "underscore", "async", "bluebird", "rxjs", "socket.io", "mongoose",
    "sequelize", "knex", "pg", "mysql", "redis", "mongodb", "graphql", "apollo",
    "request", "superagent", "cheerio", "puppeteer", "playwright", "cypress",
    "commander", "yargs", "chalk", "ora", "inquirer", "dotenv", "uuid", "nanoid",
    "date-fns", "dayjs", "ramda", "immutable", "classnames", "styled-components",
    "emotion", "tailwindcss", "bootstrap", "material-ui", "antd", "semantic-ui",
    "formik", "yup", "validator", "bcrypt", "jsonwebtoken", "passport", "helmet",
    "cors", "body-parser", "multer", "nodemailer", "sharp", "jimp", "canvas",
    "three", "d3", "chart.js", "highcharts", "leaflet", "mapbox-gl", "cesium"
]

FREE_EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "mail.com", "protonmail.com", "icloud.com", "live.com", "msn.com",
    "yandex.com", "zoho.com", "gmx.com", "fastmail.com", "tutanota.com"
]


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def calculate_entropy(data: str) -> float:
    if not data:
        return 0.0
    
    freq = {}
    for char in data:
        freq[char] = freq.get(char, 0) + 1
    
    entropy = 0.0
    length = len(data)
    for count in freq.values():
        if count > 0:
            probability = count / length
            entropy -= probability * math.log2(probability)
    
    return entropy


def find_typosquat_matches(package_name: str) -> Tuple[int, List[Dict[str, Any]]]:
    matches = []
    min_distance: int = 999
    
    for popular in POPULAR_PACKAGES:
        if popular == package_name:
            continue
        distance = levenshtein_distance(package_name.lower(), popular.lower())
        if distance <= 2:
            matches.append({
                "popular_package": popular,
                "distance": distance,
                "suspicion": "high" if distance == 1 else "medium"
            })
            if distance < min_distance:
                min_distance = distance
    
    return min_distance, matches


def is_free_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    domain = email.split("@")[-1].lower()
    return domain in FREE_EMAIL_DOMAINS


def calculate_publish_activity_score(
    releases_last_7d: int,
    releases_last_30d: int,
    is_dormant_then_sudden: bool,
    latest_age_days: int
) -> int:
    if releases_last_7d >= 5:
        return 90
    elif releases_last_7d >= 2:
        return 65
    elif is_dormant_then_sudden and latest_age_days <= 7:
        return 80
    else:
        return 10


def calculate_maintainer_score(
    maintainer_count: int,
    has_recent_maintainer: bool,
    has_github_repo: bool,
    has_free_email: bool
) -> int:
    score = 0
    
    if maintainer_count == 1:
        score += 70
    
    if has_recent_maintainer:
        score += 20
    
    if not has_github_repo:
        score += 20
    
    if has_free_email:
        score += 10
    
    return min(score, 100)


def calculate_dependency_score(
    num_deps: int,
    deprecated_deps: int,
    deps_missing_repo: int
) -> int:
    if num_deps > 50:
        base_score = 90
    elif num_deps > 20:
        base_score = 60
    elif num_deps > 5:
        base_score = 30
    else:
        base_score = 0
    
    deprecated_penalty = min(deprecated_deps * 15, 100)
    missing_repo_penalty = min(deps_missing_repo * 10, 100)
    
    return min(base_score + deprecated_penalty + missing_repo_penalty, 100)


def calculate_typosquat_score(
    min_distance: int,
    is_popular: bool
) -> int:
    if min_distance == 1:
        if not is_popular:
            return 90
        else:
            return 60
    elif min_distance == 2:
        return 30
    else:
        return 0


def calculate_tarball_score(
    has_postinstall: bool,
    has_network_commands: bool,
    has_eval_function: bool,
    has_high_entropy: bool
) -> int:
    score = 0
    
    if has_postinstall:
        score += 60
    
    if has_network_commands:
        score += 50
    
    if has_eval_function:
        score += 40
    
    if has_high_entropy:
        score += 50
    
    return min(score, 100)


def calculate_final_risk_score(
    publish_activity: int,
    maintainer: int,
    dependency: int,
    typosquat: int,
    tarball_scan: int
) -> int:
    return round(
        publish_activity * 0.25 +
        maintainer * 0.20 +
        dependency * 0.20 +
        typosquat * 0.15 +
        tarball_scan * 0.20
    )


def get_severity(risk_score: int) -> str:
    if risk_score <= 30:
        return "Low"
    elif risk_score <= 60:
        return "Medium"
    else:
        return "High"


def generate_flags(
    publish_data: Dict[str, Any],
    maintainer_data: Dict[str, Any],
    dependency_data: Dict[str, Any],
    typosquat_data: Dict[str, Any],
    tarball_data: Dict[str, Any]
) -> List[str]:
    flags = []
    
    if publish_data.get("releases_last_7d", 0) >= 5:
        flags.append("Unusual publish activity: 5+ releases in 7 days")
    if publish_data.get("is_dormant_then_sudden"):
        flags.append("Dormant package with sudden release")
    
    if maintainer_data.get("count", 0) == 1:
        flags.append("Single maintainer")
    if maintainer_data.get("has_recent_addition"):
        flags.append("Recently added maintainer")
    if not maintainer_data.get("has_github_repo", True):
        flags.append("Missing GitHub repository")
    if maintainer_data.get("has_free_email"):
        flags.append("Maintainer uses free email domain")
    
    num_deps = dependency_data.get("count", 0)
    if num_deps > 50:
        flags.append(f"High dependency count: {num_deps}")
    elif num_deps > 20:
        flags.append(f"Moderate dependency count: {num_deps}")
    
    if typosquat_data.get("min_distance", 999) <= 2:
        similar = typosquat_data.get("matches", [])
        if similar:
            flags.append(f"Possible typosquat of: {similar[0]['popular_package']}")
    
    if tarball_data.get("has_postinstall"):
        flags.append("Contains postinstall/preinstall scripts")
    if tarball_data.get("has_network_commands"):
        flags.append("Contains network commands (curl/wget/nc)")
    if tarball_data.get("has_eval_function"):
        flags.append("Contains eval() or Function() calls")
    if tarball_data.get("has_high_entropy"):
        flags.append("Contains high-entropy/obfuscated code")
    
    return flags


def parse_version_timeline(time_data: Dict[str, str]) -> List[Dict[str, str]]:
    timeline = []
    for version, timestamp in time_data.items():
        if version not in ["created", "modified"]:
            timeline.append({
                "version": version,
                "date": timestamp
            })
    timeline.sort(key=lambda x: x["date"], reverse=True)
    return timeline[:20]


def analyze_publish_activity(time_data: Dict[str, str]) -> Dict[str, Any]:
    now = datetime.utcnow()
    releases_7d = 0
    releases_30d = 0
    releases_365d = 0
    latest_date = None
    
    for version, timestamp in time_data.items():
        if version in ["created", "modified"]:
            continue
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).replace(tzinfo=None)
            age = now - dt
            
            if latest_date is None or dt > latest_date:
                latest_date = dt
            
            if age <= timedelta(days=7):
                releases_7d += 1
            if age <= timedelta(days=30):
                releases_30d += 1
            if age <= timedelta(days=365):
                releases_365d += 1
        except:
            continue
    
    total_releases = len([v for v in time_data.keys() if v not in ["created", "modified"]])
    is_dormant_then_sudden = (
        total_releases > 1 and
        releases_365d <= 2 and
        releases_30d >= 1
    )
    
    latest_age_days = (now - latest_date).days if latest_date else 999
    
    return {
        "releases_last_7d": releases_7d,
        "releases_last_30d": releases_30d,
        "is_dormant_then_sudden": is_dormant_then_sudden,
        "latest_age_days": latest_age_days,
        "latest_release_date": latest_date.isoformat() if latest_date else None
    }


def analyze_maintainers(maintainers: List[Dict[str, str]], repository: Optional[Dict]) -> Dict[str, Any]:
    has_free_email = False
    for m in maintainers:
        email = m.get("email", "")
        if is_free_email(email):
            has_free_email = True
            break
    
    has_github_repo = False
    if repository:
        repo_url = repository.get("url", "") if isinstance(repository, dict) else str(repository)
        has_github_repo = "github.com" in repo_url.lower()
    
    return {
        "count": len(maintainers),
        "maintainers": maintainers,
        "has_free_email": has_free_email,
        "has_github_repo": has_github_repo,
        "has_recent_addition": False
    }


def analyze_dependencies(dependencies: Dict[str, str]) -> Dict[str, Any]:
    return {
        "count": len(dependencies) if dependencies else 0,
        "dependencies": list(dependencies.keys()) if dependencies else [],
        "deprecated_count": 0,
        "missing_repo_count": 0
    }
