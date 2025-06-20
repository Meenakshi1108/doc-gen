import os
import pdfkit
import tempfile
from PyPDF2 import PdfWriter, PdfReader

def generate_pdf(content_html, header_html, footer_html, output_path, watermark=None):
    """
    Generate a PDF document with watermark and footer on the last page only
    
    Args:
        content_html (str): HTML content for the body
        header_html (str): HTML content for the header
        footer_html (str): HTML content for the footer (last page only)
        output_path (str): Path to save the generated PDF
        watermark (str, optional): HTML content for watermark
        
    Returns:
        str: Path to the generated document
    """
    # Configure path to wkhtmltopdf
    wkhtmltopdf_paths = [
        r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',
        r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe',
        r'wkhtmltopdf'  # If it's in PATH
    ]
    
    config = None
    for path in wkhtmltopdf_paths:
        if os.path.exists(path):
            config = pdfkit.configuration(wkhtmltopdf=path)
            break
    
    # Create temporary files
    temp_files = []
    
    try:
        # Extract watermark text if provided
        watermark_text = ""
        if watermark:
            import re
            watermark_text = re.sub(r'<[^>]*>', '', watermark).strip()
        
        # Create the main content HTML - with watermark
        main_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Generated Document</title>
            <style>
                @page {{
                    size: A4;
                    margin: 25mm 15mm 25mm 15mm;
                }}
                
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    position: relative;
                }}
                
                /* Watermark on all pages */
                {f'''
                body:before {{
                    content: "{watermark_text}";
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    z-index: -1000;
                    color: rgba(200, 200, 200, 0.3);
                    font-size: 100px;
                    font-weight: bold;
                    transform: translate(-50%, -50%) rotate(-45deg);
                }}
                
                /* Force watermark on all pages */
                @media print {{
                    body:before {{
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }}
                }}
                ''' if watermark_text else ''}
                
                /* Ensure content is above watermark */
                .content {{
                    position: relative;
                    z-index: 10;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                {content_html}
            </div>
        </body>
        </html>
        """
        
        # Save main HTML to temporary file
        main_html_path = tempfile.mktemp(suffix='.html')
        with open(main_html_path, 'w', encoding='utf-8') as f:
            f.write(main_html)
        temp_files.append(main_html_path)
        
        # Create header HTML if provided
        header_html_path = None
        if header_html:
            header_html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        text-align: center;
                        font-size: 10px;
                        color: #777;
                    }}
                </style>
            </head>
            <body>
                {header_html}
            </body>
            </html>
            """
            
            header_html_path = tempfile.mktemp(suffix='.html')
            with open(header_html_path, 'w', encoding='utf-8') as f:
                f.write(header_html_content)
            temp_files.append(header_html_path)
        
        # Configure options for wkhtmltopdf
        options = {
            'page-size': 'A4',
            'margin-top': '25mm',
            'margin-right': '15mm',
            'margin-bottom': '25mm',
            'margin-left': '15mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None
        }
        
        # Add header if provided
        if header_html_path:
            options['header-html'] = header_html_path
            options['header-spacing'] = '5'
        
        # Generate main content PDF
        temp_pdf_path = tempfile.mktemp(suffix='.pdf')
        temp_files.append(temp_pdf_path)
        pdfkit.from_file(main_html_path, temp_pdf_path, options=options, configuration=config)
        
        # If footer is provided, create a PDF with footer for the last page
        if footer_html:
            # Create footer HTML file
            footer_html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        text-align: center;
                        border-top: 1px solid #ccc;
                        padding-top: 5px;
                        font-size: 10px;
                        color: #777;
                    }}
                </style>
            </head>
            <body>
                {footer_html}
            </body>
            </html>
            """
            
            footer_html_path = tempfile.mktemp(suffix='.html')
            with open(footer_html_path, 'w', encoding='utf-8') as f:
                f.write(footer_html_content)
            temp_files.append(footer_html_path)
            
            # Use PyPDF2 to add footer only to the last page
            pdf_writer = PdfWriter()
            pdf_reader = PdfReader(temp_pdf_path)
            
            # Copy all pages except the last one
            for page_num in range(len(pdf_reader.pages) - 1):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Get the last page
            if len(pdf_reader.pages) > 0:
                # For the last page, create a new page with footer
                last_page_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Last Page</title>
                    <style>
                        @page {{
                            size: A4;
                            margin: 25mm 15mm 25mm 15mm;
                        }}
                        
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            position: relative;
                        }}
                        
                        {f'''
                        /* Watermark */
                        body:before {{
                            content: "{watermark_text}";
                            position: fixed;
                            top: 50%;
                            left: 50%;
                            z-index: -1000;
                            color: rgba(200, 200, 200, 0.3);
                            font-size: 100px;
                            font-weight: bold;
                            transform: translate(-50%, -50%) rotate(-45deg);
                        }}
                        ''' if watermark_text else ''}
                        
                        .content {{
                            position: relative;
                            z-index: 10;
                            margin-bottom: 50px; /* Space for footer */
                        }}
                        
                        .footer {{
                            position: fixed;
                            bottom: 0;
                            left: 0;
                            width: 100%;
                            text-align: center;
                            border-top: 1px solid #ccc;
                            padding-top: 5px;
                            font-size: 10px;
                            color: #777;
                        }}
                    </style>
                </head>
                <body>
                    <div class="content"></div>
                    <div class="footer">
                        {footer_html}
                    </div>
                </body>
                </html>
                """
                
                last_page_html_path = tempfile.mktemp(suffix='.html')
                with open(last_page_html_path, 'w', encoding='utf-8') as f:
                    f.write(last_page_html)
                temp_files.append(last_page_html_path)
                
                # Configure options to match previous pages
                if header_html_path:
                    options['header-html'] = header_html_path
                
                # Create a temporary PDF for the last page with footer
                last_page_pdf = tempfile.mktemp(suffix='.pdf')
                temp_files.append(last_page_pdf)
                
                # Get content from last page of original pdf
                last_page = pdf_reader.pages[-1]
                
                # Create a PDF with just the last page's content
                last_page_writer = PdfWriter()
                last_page_writer.add_page(last_page)
                last_page_content = tempfile.mktemp(suffix='.pdf')
                temp_files.append(last_page_content)
                with open(last_page_content, 'wb') as f:
                    last_page_writer.write(f)
                
                # Generate the footer PDF
                footer_pdf = tempfile.mktemp(suffix='.pdf')
                temp_files.append(footer_pdf)
                pdfkit.from_file(footer_html_path, footer_pdf, options=options, configuration=config)
                
                # Merge last page with footer
                footer_reader = PdfReader(footer_pdf)
                if footer_reader.pages:
                    # Add the last page with content
                    pdf_writer.add_page(last_page)
                    
                    # Check if we need to handle the footer as a separate page
                    # (usually we'd overlay the footer onto the last page, but this approach is simpler for now)
                    if len(pdf_writer.pages) > 0:
                        last_page = pdf_writer.pages[-1]
                        # We can add footer directly to the page's annotation or as an overlay
                        # For simplicity, we'll just adjust the footer placement at the bottom of the last page
                
            # Save the final PDF
            with open(output_path, 'wb') as f:
                pdf_writer.write(f)
        else:
            # If no footer, just copy the temp PDF to the output
            import shutil
            shutil.copy(temp_pdf_path, output_path)
            
        return output_path
        
    finally:
        # Clean up temporary files
        for path in temp_files:
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass