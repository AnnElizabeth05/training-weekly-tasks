import pytest
from data_access import get_dataset_path
from data_access import validate_access_request
from data_access import verify_dataset_completeness


def test_get_dataset_path():
    """Test: Get path for existing dataset"""
    path = get_dataset_path("sales_data")
    assert path == "/mnt/data/sales/2025/"


def test_get_dataset_path_empty():
    """Test: Empty dataset name returns None"""
    path = get_dataset_path("")
    assert path is None


def test_get_dataset_path_not_found():
    """Test: Unknown dataset returns None"""
    path = get_dataset_path("marketing_data")
    assert path is None


def test_validate_access_request_valid():
    """Test: Complete request passes validation"""
    valid, missing = validate_access_request(
        "sales_data",
        "john_doe",
        "Need data for monthly reporting"
    )
    assert valid is True
    assert missing == []


def test_validate_access_request_all_empty():
    """Test: All fields empty fails validation"""
    valid, missing = validate_access_request("", "", "")
    assert valid is False
    assert len(missing) == 3
    assert "dataset_name" in missing
    assert "user_id" in missing
    assert "purpose" in missing


def test_validate_access_request_missing_purpose():
    """Test: Missing purpose fails validation"""
    valid, missing = validate_access_request("sales_data", "john_doe", "")
    assert valid is False
    assert "purpose" in missing
    assert len(missing) == 1


@pytest.mark.parametrize(
    "actual, expected, result",
    [
        (8, 8, True),      # Complete - exact match
        (6, 8, False),     # Incomplete - missing files
        (0, 8, False),     # Empty dataset
        (10, 8, True),     # Extra files - still complete
        (4, 4, True),      # Smaller dataset - complete
    ]
)
def test_verify_dataset_completeness(actual, expected, result):
    """Parametrized test for completeness check"""
    outcome = verify_dataset_completeness("sales_data", actual, expected)
    assert outcome is result


def test_verify_dataset_completeness_empty_name():
    """Test: Empty dataset name returns False"""
    result = verify_dataset_completeness("", 8, 8)
    assert result is False