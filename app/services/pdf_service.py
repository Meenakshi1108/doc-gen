import os
import pdfkit
import tempfile

def generate_pdf(content_html, header_html, footer_html, output_path, watermark=None):
    """
    Generate a PDF document from HTML content using pdfkit (wkhtmltopdf)
    """
    # Configure the path to wkhtmltopdf
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
    
    # Create temporary files for header and footer
    header_path = None
    footer_path = None
    html_path = None
    
    try:
        # Create watermark style if provided
        watermark_style = ""
        watermark_content = ""
        
        if watermark:
            # Extract plain text from watermark HTML if needed
            import re
            watermark_text = re.sub(r'<[^>]*>', '', watermark).strip()
            
            # Create a better positioned watermark that appears on all pages
            watermark_style = """
                /* Use a pseudo-element to create the watermark background */
                .watermark-container {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: -1000;
                    pointer-events: none;
                }
                
                .watermark {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(-45deg);
                    font-size: 120px;
                    color: rgba(200, 200, 200, 0.3);
                    white-space: nowrap;
                    z-index: -1000;
                }
            """
            
            watermark_content = f"""
                <div class="watermark-container">
                    <div class="watermark">{watermark_text}</div>
                </div>
            """
        
        # Save header HTML to temporary file if provided
        if header_html:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
                f.write(f"<html><head><style></style></head><body>{header_html}</body></html>")
                header_path = f.name
        
        # Save footer HTML to temporary file if provided - for last page only
        if footer_html:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
                # We'll use a special script to show footer only on last page
                last_page_footer = f"""
                <html>
                <head>
                    <style>
                        /* Hide footer on non-last pages */
                        .footer-content {{ display: none; }}
                        /* Show footer only when we detect it's the last page */
                        .footer-content.is-last-page {{ display: block; }}
                    </style>
                    <script>
                        function isLastPage() {{
                            // Get the current page number from wkhtmltopdf's vars
                            var page = parseInt(document.querySelector('.page').innerHTML);
                            var topage = parseInt(document.querySelector('.topage').innerHTML);
                            
                            // If current page equals total pages, we're on the last page
                            if (page === topage) {{
                                document.querySelector('.footer-content').classList.add('is-last-page');
                            }}
                        }}
                    </script>
                </head>
                <body onload="isLastPage()">
                    <!-- Placeholders for wkhtmltopdf to insert page numbers -->
                    <span style="display: none;" class="page"></span>
                    <span style="display: none;" class="topage"></span>
                    
                    <!-- The actual footer content -->
                    <div class="footer-content">
                        {footer_html}
                    </div>
                </body>
                </html>
                """
                
                f.write(last_page_footer)
                footer_path = f.name
        
        # Create a complete HTML document with the watermark properly positioned
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Generated Document</title>
            <style>
                {watermark_style}
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    position: relative; 
                    z-index: 1;
                }}
                
                /* Ensure all content is above the watermark */
                #content {{
                    position: relative;
                    z-index: 10;
                }}
            </style>
        </head>
        <body>
            {watermark_content}
            <div id="content">{content_html}</div>
        </body>
        </html>
        """
        
        # Save the HTML to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
            f.write(full_html)
            html_path = f.name
        
        # Configure options for wkhtmltopdf
        options = {
            'page-size': 'A4',
            'margin-top': '25mm',
            'margin-right': '15mm',
            'margin-bottom': '25mm',
            'margin-left': '15mm',
            'encoding': 'UTF-8',
            'javascript-delay': '1000',  # Wait for JS to execute
            'enable-local-file-access': None,
            'print-media-type': None,
            'enable-javascript': None,
            'no-stop-slow-scripts': None
        }
        
        # Add header and footer if available
        if header_path:
            options['header-html'] = header_path
            options['header-spacing'] = '5'
        
        if footer_path:
            options['footer-html'] = footer_path
            options['footer-spacing'] = '5'
            
            # These variables will be available in the footer HTML
            options['footer-left'] = '[page]'
            options['footer-right'] = '[topage]'
        
        # Generate PDF using wkhtmltopdf
        pdfkit.from_file(html_path, output_path, options=options, configuration=config)
        
        return output_path
    
    finally:
        # Clean up temporary files
        for path in [header_path, footer_path, html_path]:
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except:
                    pass  # Ignore errors on cleanup