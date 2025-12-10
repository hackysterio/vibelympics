import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from audit import (
    levenshtein_distance,
    calculate_entropy,
    find_typosquat_matches,
    is_free_email,
    calculate_publish_activity_score,
    calculate_maintainer_score,
    calculate_dependency_score,
    calculate_typosquat_score,
    calculate_tarball_score,
    calculate_final_risk_score,
    get_severity,
    POPULAR_PACKAGES
)


class TestLevenshteinDistance:
    def test_identical_strings(self):
        assert levenshtein_distance("hello", "hello") == 0
    
    def test_single_insertion(self):
        assert levenshtein_distance("hello", "helo") == 1
    
    def test_single_deletion(self):
        assert levenshtein_distance("helo", "hello") == 1
    
    def test_single_substitution(self):
        assert levenshtein_distance("hello", "hallo") == 1
    
    def test_multiple_edits(self):
        assert levenshtein_distance("kitten", "sitting") == 3
    
    def test_empty_string(self):
        assert levenshtein_distance("hello", "") == 5
        assert levenshtein_distance("", "hello") == 5
        assert levenshtein_distance("", "") == 0
    
    def test_typosquat_examples(self):
        assert levenshtein_distance("expres", "express") == 1
        assert levenshtein_distance("expresss", "express") == 1
        assert levenshtein_distance("lodahs", "lodash") == 2
        assert levenshtein_distance("reakt", "react") == 1


class TestEntropy:
    def test_empty_string(self):
        assert calculate_entropy("") == 0.0
    
    def test_single_char_repeated(self):
        assert calculate_entropy("aaaaaaa") == 0.0
    
    def test_two_chars_equal_frequency(self):
        entropy = calculate_entropy("abababab")
        assert 0.9 < entropy < 1.1
    
    def test_random_string_high_entropy(self):
        high_entropy_string = "aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0"
        entropy = calculate_entropy(high_entropy_string)
        assert entropy > 4.0
    
    def test_base64_like_string(self):
        base64_str = "SGVsbG8gV29ybGQhIFRoaXMgaXMgYSB0ZXN0IHN0cmluZyB3aXRoIGhpZ2ggZW50cm9weQ=="
        entropy = calculate_entropy(base64_str)
        assert entropy > 3.5


class TestTyposquatDetection:
    def test_exact_match_no_flag(self):
        min_dist, matches = find_typosquat_matches("express")
        assert all(m["popular_package"] != "express" for m in matches)
    
    def test_one_char_off(self):
        min_dist, matches = find_typosquat_matches("expres")
        assert min_dist == 1
        assert len(matches) > 0
        assert any(m["popular_package"] == "express" for m in matches)
    
    def test_two_chars_off(self):
        min_dist, matches = find_typosquat_matches("expss")
        assert min_dist <= 2
        assert len(matches) >= 0
    
    def test_completely_different(self):
        min_dist, matches = find_typosquat_matches("xyzabc123")
        assert min_dist == 999
        assert len(matches) == 0


class TestFreeEmail:
    def test_gmail(self):
        assert is_free_email("user@gmail.com") == True
    
    def test_yahoo(self):
        assert is_free_email("user@yahoo.com") == True
    
    def test_hotmail(self):
        assert is_free_email("user@hotmail.com") == True
    
    def test_company_email(self):
        assert is_free_email("user@company.com") == False
    
    def test_empty_email(self):
        assert is_free_email("") == False
    
    def test_invalid_email(self):
        assert is_free_email("invalid") == False


class TestPublishActivityScore:
    def test_many_releases_7d(self):
        score = calculate_publish_activity_score(5, 10, False, 1)
        assert score == 90
    
    def test_moderate_releases_7d(self):
        score = calculate_publish_activity_score(2, 5, False, 3)
        assert score == 65
    
    def test_dormant_then_sudden(self):
        score = calculate_publish_activity_score(1, 1, True, 3)
        assert score == 80
    
    def test_normal_activity(self):
        score = calculate_publish_activity_score(0, 1, False, 30)
        assert score == 10


class TestMaintainerScore:
    def test_single_maintainer(self):
        score = calculate_maintainer_score(1, False, True, False)
        assert score == 70
    
    def test_multiple_maintainers(self):
        score = calculate_maintainer_score(3, False, True, False)
        assert score == 0
    
    def test_single_with_free_email(self):
        score = calculate_maintainer_score(1, False, True, True)
        assert score == 80
    
    def test_missing_github(self):
        score = calculate_maintainer_score(2, False, False, False)
        assert score == 20
    
    def test_all_flags(self):
        score = calculate_maintainer_score(1, True, False, True)
        assert score == 100


class TestDependencyScore:
    def test_many_deps(self):
        score = calculate_dependency_score(60, 0, 0)
        assert score == 90
    
    def test_moderate_deps(self):
        score = calculate_dependency_score(25, 0, 0)
        assert score == 60
    
    def test_few_deps(self):
        score = calculate_dependency_score(8, 0, 0)
        assert score == 30
    
    def test_minimal_deps(self):
        score = calculate_dependency_score(3, 0, 0)
        assert score == 0
    
    def test_deprecated_deps(self):
        score = calculate_dependency_score(10, 3, 0)
        assert score == 30 + 45


class TestTyposquatScore:
    def test_distance_1_unpopular(self):
        score = calculate_typosquat_score(1, False)
        assert score == 90
    
    def test_distance_1_popular(self):
        score = calculate_typosquat_score(1, True)
        assert score == 60
    
    def test_distance_2(self):
        score = calculate_typosquat_score(2, False)
        assert score == 30
    
    def test_no_match(self):
        score = calculate_typosquat_score(999, False)
        assert score == 0


class TestTarballScore:
    def test_postinstall(self):
        score = calculate_tarball_score(True, False, False, False)
        assert score == 60
    
    def test_network_commands(self):
        score = calculate_tarball_score(False, True, False, False)
        assert score == 50
    
    def test_eval_function(self):
        score = calculate_tarball_score(False, False, True, False)
        assert score == 40
    
    def test_high_entropy(self):
        score = calculate_tarball_score(False, False, False, True)
        assert score == 50
    
    def test_multiple_flags_capped(self):
        score = calculate_tarball_score(True, True, True, True)
        assert score == 100


class TestFinalScore:
    def test_all_low(self):
        score = calculate_final_risk_score(10, 0, 0, 0, 0)
        assert score == round(10 * 0.25)
    
    def test_all_high(self):
        score = calculate_final_risk_score(100, 100, 100, 100, 100)
        assert score == 100
    
    def test_weighted_calculation(self):
        score = calculate_final_risk_score(40, 50, 60, 70, 80)
        expected = round(40*0.25 + 50*0.20 + 60*0.20 + 70*0.15 + 80*0.20)
        assert score == expected


class TestSeverity:
    def test_low(self):
        assert get_severity(0) == "Low"
        assert get_severity(30) == "Low"
    
    def test_medium(self):
        assert get_severity(31) == "Medium"
        assert get_severity(60) == "Medium"
    
    def test_high(self):
        assert get_severity(61) == "High"
        assert get_severity(100) == "High"


class TestPopularPackages:
    def test_list_has_minimum_count(self):
        assert len(POPULAR_PACKAGES) >= 50
    
    def test_common_packages_included(self):
        assert "express" in POPULAR_PACKAGES
        assert "react" in POPULAR_PACKAGES
        assert "lodash" in POPULAR_PACKAGES
        assert "axios" in POPULAR_PACKAGES
