from app.services.pdf_service import generate_pdf
from app.services.docx_service import generate_docx

def generate_document(content_html, header_html, footer_html, document_type, output_path, watermark=None):
    """
    Generate a document based on the specified type
    
    Args:
        content_html (str): HTML content for the body
        header_html (str): HTML content for the header
        footer_html (str): HTML content for the footer
        document_type (str): "pdf" or "docx"
        output_path (str): Path where the document should be saved
        watermark (str, optional): HTML content for watermark
        
    Returns:
        str: Path to the generated document
    """
    if document_type.lower() == 'pdf':
        return generate_pdf(content_html, header_html, footer_html, output_path, watermark)
    elif document_type.lower() == 'docx':
        return generate_docx(content_html, header_html, footer_html, output_path, watermark)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")