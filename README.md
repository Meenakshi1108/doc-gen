# Document Generation Service

A Flask-based microservice for generating PDF and DOCX documents from HTML content with support for headers, footers, and watermarks.

## Features

- **Multiple Document Formats**: Generate both PDF and DOCX documents from HTML content
- **Header Support**: Add custom headers to each page of your documents
- **Footer Support**: Add custom footers to the last page of documents
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
- **PyPDF2**: PDF manipulation

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

```
python -m app.main
```

The service will start on http://localhost:5000 with API documentation available at http://localhost:5000/api/docs

## API Usage

### Generate Document

**Endpoint**: `POST /api/v1/generate`

**Request Body**:
```json
{
  "content_html": "<p>Main document content</p>",
  "header_html": "<p>Header text</p>",
  "footer_html": "<p>Footer text</p>",
  "document_type": "pdf",
  "watermark": "CONFIDENTIAL"
}
```

**Parameters**:
- `content_html` (required): HTML content for the document body
- `header_html` (optional): HTML content for the header
- `footer_html` (optional): HTML content for the footer
- `document_type` (required): Output format - either "pdf" or "docx"
- `watermark` (optional): Text for watermark

**Response**: 
- `200 OK`: Returns the generated document as a file download
- `400 Bad Request`: Validation error
- `500 Internal Server Error`: Processing error

## Document Formatting

### Page Breaks

To add page breaks in your document content:
```html
<p>Content before page break</p>
<p style="page-break-before: always;">Content after page break</p>
```

### Tables

Standard HTML tables are supported:
```html
<table>
  <tr>
    <th>Header 1</th>
    <th>Header 2</th>
  </tr>
  <tr>
    <td>Data 1</td>
    <td>Data 2</td>
  </tr>
</table>
```

## Examples

### Creating a PDF with Header and Footer

```python
import requests
import json

url = "http://localhost:5000/api/v1/generate"
payload = {
    "content_html": "<h1>Sample Document</h1><p>This is a sample document.</p>",
    "header_html": "<p>Company Name - Confidential</p>",
    "footer_html": "<p>Page 1</p>",
    "document_type": "pdf"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)

with open("output.pdf", "wb") as f:
    f.write(response.content)
```

### Creating a DOCX with Watermark

```python
import requests
import json

url = "http://localhost:5000/api/v1/generate"
payload = {
    "content_html": "<h1>Sample Document</h1><p>This is a sample document.</p>",
    "document_type": "docx",
    "watermark": "DRAFT"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)

with open("output.docx", "wb") as f:
    f.write(response.content)
```

## Architecture

The service follows a layered architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Service Layer**: Implements document generation logic
3. **Validation Layer**: Validates input parameters
4. **Utilities**: Manages resources like temporary files

## Security Considerations

- No authentication is included - add your own authentication layer for production use

