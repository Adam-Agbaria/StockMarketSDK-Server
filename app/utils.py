def validate_stock_data(data):
    """
    Validate incoming stock data.
    Ensure all required fields are present and correctly formatted.
    """
    required_fields = ["symbol", "date", "open_price", "high", "low", "close"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, "Data is valid"
