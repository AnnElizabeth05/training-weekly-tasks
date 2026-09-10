


class AccessError(Exception):
    """Raised when a dataset access request fails."""
    pass


class AccessRequest:
    """A request from an intern to access a dataset."""

    def __init__(self, dataset_name, requester_id, reason):
        self.dataset_name = dataset_name
        self.requester_id = requester_id
        self.reason = reason
        self.status = "pending"

    def is_valid(self):
        """Check if the request has all required fields."""
        return bool(self.dataset_name and self.requester_id and self.reason)

    def submit(self):
        """Submit the request, or raise an error if invalid."""
        if not self.is_valid():
            raise AccessError(
                f"Request from {self.requester_id} is missing required fields"
            )
        self.status = "submitted"
        return True


# Part 2 - Connector hierarchy

class DatasetConnector:
    """Base class for any dataset connector."""

    def fetch(self):
        raise NotImplementedError("Subclasses must implement fetch()")


class SharePointConnector(DatasetConnector):
    def fetch(self):
        return "Fetched from SharePoint"


class TeamsConnector(DatasetConnector):
    def fetch(self):
        return "Fetched from Teams"


class LoggingMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")


class LoggedSharePointConnector(LoggingMixin, SharePointConnector):
    def fetch(self):
        self.log("Fetching from SharePoint")
        return super().fetch()


# Quick check when run directly
if __name__ == "__main__":
    # Part 1 - two independent requests
    req1 = AccessRequest("sales_data", "intern_001", "Need for Q1 report")
    req2 = AccessRequest("customer_data", "intern_002", "Need for analysis")

    print(f"req1 valid: {req1.is_valid()}")
    print(f"req2 valid: {req2.is_valid()}")

    try:
        req1.submit()
        print(f"req1 status: {req1.status}")
    except AccessError as e:
        print(f"Caught: {e}")

    # Part 2 - connector and MRO
    connector = LoggedSharePointConnector()
    print(connector.fetch())
    print(f"MRO: {[c.__name__ for c in LoggedSharePointConnector.__mro__]}")