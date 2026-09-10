
Tests for the dataset access system.
import pytest
from approval_system import (
    AccessRequest,
    AccessError,
    SharePointConnector,
    TeamsConnector,
    LoggedSharePointConnector,
)


def test_valid_request():
    req = AccessRequest("sales_data", "intern_001", "Need for Q1 report")
    assert req.is_valid() is True


def test_invalid_request_missing_reason():
    req = AccessRequest("sales_data", "intern_001", "")
    assert req.is_valid() is False


def test_submit_valid_request():
    req = AccessRequest("sales_data", "intern_001", "Need for Q1 report")
    assert req.submit() is True
    assert req.status == "submitted"


def test_submit_invalid_request_raises():
    req = AccessRequest("", "intern_001", "Need data")
    with pytest.raises(AccessError):
        req.submit()


def test_two_requests_are_independent():
    req1 = AccessRequest("sales_data", "intern_001", "Q1 report")
    req2 = AccessRequest("customer_data", "intern_002", "Analysis")

    req1.submit()

    assert req1.status == "submitted"
    assert req2.status == "pending"


def test_sharepoint_connector_fetch():
    connector = SharePointConnector()
    assert connector.fetch() == "Fetched from SharePoint"


def test_teams_connector_fetch():
    connector = TeamsConnector()
    assert connector.fetch() == "Fetched from Teams"


def test_logged_connector_uses_mixin():
    connector = LoggedSharePointConnector()
    assert connector.fetch() == "Fetched from SharePoint"


def test_mro_order():
    mro_names = [c.__name__ for c in LoggedSharePointConnector.__mro__]
    assert mro_names == [
        "LoggedSharePointConnector",
        "LoggingMixin",
        "SharePointConnector",
        "DatasetConnector",
        "object",
    ]