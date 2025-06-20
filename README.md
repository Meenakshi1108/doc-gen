# Document Generation Service

A Flask-based microservice for generating PDF and DOCX documents from HTML content with support for headers, footers, and watermarks.

## Features

- **Multiple Document Formats**: Generate both PDF and DOCX documents from HTML content
- **Header Support**: Add custom headers to each page of your documents
- **Footer Support**: Add custom footers to the last page of documents only
- **Watermarking**: Apply text watermarks across all document pages
- **Page Breaks**: Control document pagination with HTML-based page breaks
- **RESTful API**: Simple HTTP API with proper validation and error responses
- **API Documentation**: Interactive API docs with Swagger UI

## Tech Stack

- **Flask**: Lightweight Python web framework
- **Flask-RestX**: API development and documentation
- **wkhtmltopdf/pdfkit**: HTML to PDF conversion
- **python-docx**: HTML to DOCX conversion
- **BeautifulSoup**: HTML parsing
- **PyPDF2**: PDF manipulation for last-page footer implementation

## Getting Started

### Prerequisites

- Python 3.6+
- wkhtmltopdf installed for PDF generation

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/docgen.git
   cd docgen
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install wkhtmltopdf:
   - Windows: Download and install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
   - Linux: `sudo apt-get install wkhtmltopdf`
   - macOS: `brew install wkhtmltopdf`

### Running the Service

1. Start the service:
   ```
   python -m app.main
   ```

2. The service will be available at:
   - API Endpoint: `http://localhost:5000/api/v1/generate`
   - API Documentation: `http://localhost:5000/api/docs`

## API Usage

### Generate Document

**Endpoint**: `POST /api/v1/generate`

**Request Body**:
```json
{
  "content_html": "<h1>Document Title</h1><p>This is the document content.</p>",
  "header_html": "<div>Header Content</div>",
  "footer_html": "<div>Footer Content - Only on Last Page</div>",
  "document_type": "pdf", /* or "docx" */
  "watermark": "CONFIDENTIAL"
}
```

**Response**: The generated document file as a download attachment.

## Examples

### HTML Content with Page Breaks

To insert page breaks in your content, use the following HTML:

```html
<p>First page content</p>
<p style="page-break-before: always;">Second page content</p>
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input parameters
- `500 Internal Server Error`: Server-side processing errors

## Project Structure

- `app/main.py`: Application entry point
- `app/api/document_api.py`: API routes and request handling
- `app/services/document_service.py`: Main document generation service
- `app/services/pdf_service.py`: PDF generation implementation
- `app/services/docx_service.py`: DOCX generation implementation
- `app/services/docx_watermark.py`: DOCX watermarking implementation
- `app/validators/input_validator.py`: Request validation
- `app/utils/file_cleanup.py`: Temporary file management


