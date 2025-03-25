def validate_document_request(data):
    """
    Validates the document generation request data
    
    Args:
        data (dict): The request data
        
    Returns:
        bool|str: True if valid, error message if invalid
    """
    # Check if required fields are present
    required_fields = ['content_html', 'document_type']
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
    
    # Validate document type
    valid_doc_types = ['pdf', 'docx']
    if data['document_type'].lower() not in valid_doc_types:
        return f"Invalid document_type: {data['document_type']}. Must be one of {valid_doc_types}"
    
    # Ensure HTML content fields are strings
    html_fields = ['content_html', 'header_html', 'footer_html']
    for field in html_fields:
        if field in data and not isinstance(data[field], str):
            return f"Field {field} must be a string"
            
    # Validate watermark if present
    if 'watermark' in data and data['watermark'] is not None:
        if not isinstance(data['watermark'], str):
            return "Watermark must be a string"
    
    return True