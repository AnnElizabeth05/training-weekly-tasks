def get_dataset_path(dataset_name):
    """
    Retrieve the file path for a given dataset.
    Returns None if the dataset doesn't exist in the catalog.
    """
    if not dataset_name:
        return None
    
    # Catalog of available datasets with their storage locations
    dataset_catalog = {
        "sales_data": "/mnt/data/sales/2025/",
        "customer_data": "/mnt/data/customers/master/",
        "inventory_data": "/mnt/data/inventory/current/"
    }
    
    return dataset_catalog.get(dataset_name)


def validate_access_request(dataset_name, user_id, purpose):
    """
    Validate if an access request has all required information.
    Returns (True, []) if valid, (False, missing_fields) if invalid.
    """
    missing = []
    
    if not dataset_name:
        missing.append("dataset_name")
    if not user_id:
        missing.append("user_id")
    if not purpose:
        missing.append("purpose")
    
    if missing:
        return False, missing
    
    return True, []


def verify_dataset_completeness(dataset_name, actual_files, expected_files):
    """
    Check if a dataset contains all expected files.
    Returns True if complete, False otherwise.
    """
    if not dataset_name:
        return False
    
    return actual_files >= expected_files