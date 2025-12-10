import pytest
import sys
import os
from unittest.mock import patch, AsyncMock, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


MOCK_NPM_RESPONSE = {
    "name": "test-package",
    "description": "A test package for unit testing",
    "dist-tags": {
        "latest": "1.0.0"
    },
    "versions": {
        "1.0.0": {
            "name": "test-package",
            "version": "1.0.0",
            "dependencies": {
                "lodash": "^4.17.21"
            },
            "devDependencies": {},
            "repository": {
                "type": "git",
                "url": "git+https://github.com/test/test-package.git"
            },
            "dist": {
                "tarball": "https://registry.npmjs.org/test-package/-/test-package-1.0.0.tgz"
            },
            "scripts": {},
            "license": "MIT"
        }
    },
    "time": {
        "created": "2024-01-01T00:00:00.000Z",
        "modified": "2024-06-01T00:00:00.000Z",
        "1.0.0": "2024-06-01T00:00:00.000Z"
    },
    "maintainers": [
        {"name": "testuser", "email": "testuser@company.com"}
    ],
    "repository": {
        "type": "git",
        "url": "git+https://github.com/test/test-package.git"
    },
    "homepage": "https://github.com/test/test-package"
}


@pytest.fixture
def mock_registry_response():
    return MOCK_NPM_RESPONSE.copy()


class TestRegistryParsing:
    def test_extract_package_info(self, mock_registry_response):
        from registry import extract_package_info
        
        info = extract_package_info(mock_registry_response)
        
        assert info["name"] == "test-package"
        assert info["latest_version"] == "1.0.0"
        assert "1.0.0" in info["versions"]
        assert len(info["maintainers"]) == 1
        assert info["repository"] is not None
    
    def test_extract_package_info_with_error(self):
        from registry import extract_package_info
        
        error_response = {"error": "Package not found"}
        info = extract_package_info(error_response)
        
        assert "error" in info


class TestPublishActivityAnalysis:
    def test_analyze_publish_activity(self, mock_registry_response):
        from audit import analyze_publish_activity
        
        result = analyze_publish_activity(mock_registry_response["time"])
        
        assert "releases_last_7d" in result
        assert "releases_last_30d" in result
        assert "is_dormant_then_sudden" in result
        assert "latest_age_days" in result


class TestMaintainerAnalysis:
    def test_analyze_maintainers_with_github(self, mock_registry_response):
        from audit import analyze_maintainers
        
        result = analyze_maintainers(
            mock_registry_response["maintainers"],
            mock_registry_response["repository"]
        )
        
        assert result["count"] == 1
        assert result["has_github_repo"] == True
        assert result["has_free_email"] == False
    
    def test_analyze_maintainers_free_email(self):
        from audit import analyze_maintainers
        
        maintainers = [{"name": "user", "email": "user@gmail.com"}]
        
        result = analyze_maintainers(maintainers, None)
        
        assert result["has_free_email"] == True
        assert result["has_github_repo"] == False


class TestDependencyAnalysis:
    def test_analyze_dependencies(self, mock_registry_response):
        from audit import analyze_dependencies
        
        deps = mock_registry_response["versions"]["1.0.0"]["dependencies"]
        result = analyze_dependencies(deps)
        
        assert result["count"] == 1
        assert "lodash" in result["dependencies"]
    
    def test_analyze_empty_dependencies(self):
        from audit import analyze_dependencies
        
        result = analyze_dependencies({})
        
        assert result["count"] == 0
        assert result["dependencies"] == []


class TestVersionTimeline:
    def test_parse_version_timeline(self, mock_registry_response):
        from audit import parse_version_timeline
        
        timeline = parse_version_timeline(mock_registry_response["time"])
        
        assert len(timeline) > 0
        assert all("version" in item for item in timeline)
        assert all("date" in item for item in timeline)


@pytest.mark.asyncio
class TestAsyncFunctions:
    async def test_fetch_package_metadata_mocked(self):
        from registry import fetch_package_metadata
        
        with patch('registry.httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = MOCK_NPM_RESPONSE
            mock_response.raise_for_status = MagicMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
            mock_client_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value = mock_client_instance
            
            with patch('registry.get_cached_registry', return_value=None):
                with patch('registry.set_cached_registry'):
                    result = await fetch_package_metadata("test-package")
            
            assert result["name"] == "test-package"
    
    async def test_fetch_package_not_found(self):
        from registry import fetch_package_metadata
        
        with patch('registry.httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 404
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
            mock_client_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value = mock_client_instance
            
            with patch('registry.get_cached_registry', return_value=None):
                result = await fetch_package_metadata("nonexistent-package-xyz")
            
            assert "error" in result


class TestTarballScanner:
    def test_scan_nonexistent_tarball(self):
        from tarball_scanner import scan_tarball
        
        result = scan_tarball("/nonexistent/path/file.tgz")
        
        assert result["has_postinstall"] == False
        assert result["has_network_commands"] == False
        assert result["has_eval_function"] == False
        assert result["has_high_entropy"] == False
    
    def test_get_tarball_summary_empty(self):
        from tarball_scanner import get_tarball_summary
        
        findings = {
            "has_postinstall": False,
            "has_network_commands": False,
            "has_eval_function": False,
            "has_high_entropy": False,
            "install_scripts": [],
            "network_patterns": [],
            "eval_patterns": [],
            "high_entropy_strings": []
        }
        
        summary = get_tarball_summary(findings)
        assert len(summary) == 0
    
    def test_get_tarball_summary_with_findings(self):
        from tarball_scanner import get_tarball_summary
        
        findings = {
            "has_postinstall": True,
            "has_network_commands": True,
            "has_eval_function": False,
            "has_high_entropy": False,
            "install_scripts": [{"name": "postinstall", "content": "echo test"}],
            "network_patterns": [{"file": "test.js", "pattern": "curl", "snippet": "..."}],
            "eval_patterns": [],
            "high_entropy_strings": []
        }
        
        summary = get_tarball_summary(findings)
        assert len(summary) == 2
