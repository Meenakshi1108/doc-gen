import os
import pdfkit
import tempfile

def generate_pdf(content_html, header_html, footer_html, output_path, watermark=None):
    """
    Generate a PDF document with correct watermark and last-page-only footer
    Using a simpler, more reliable approach with wkhtmltopdf's built-in features
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
        # Extract watermark text
        watermark_text = ""
        if watermark:
            import re
            watermark_text = re.sub(r'<[^>]*>', '', watermark).strip()
        
        # Create the complete HTML with watermark and content
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
                
                .content {{
                    position: relative;
                    z-index: 10;
                }}
                
                /* Watermark styling */
                body::before {{
                    content: "{watermark_text}";
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 100px;
                    color: rgba(200, 200, 200, 0.3);
                    transform: rotate(-45deg);
                    pointer-events: none;
                    z-index: -1000;
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
        
        # Save main HTML to a temporary file
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
                        padding: 5px;
                        text-align: center;
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
        
        # Create footer HTML with JavaScript to only show on last page
        footer_html_path = None
        if footer_html:
            footer_html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 5px;
                        text-align: center;
                    }}
                    
                    .footer-content {{
                        /* Start hidden */
                        display: none;
                    }}
                </style>
                <script>
                    function checkLastPage() {{
                        /* Get page numbers */
                        var page = parseInt(document.getElementById('page').innerText);
                        var topage = parseInt(document.getElementById('topage').innerText);
                        
                        /* Show footer only on last page */
                        if (page === topage) {{
                            document.getElementById('footer').style.display = 'block';
                        }}
                    }}
                </script>
            </head>
            <body onload="checkLastPage()">
                <!-- Hidden elements with page numbers -->
                <span id="page" style="display:none;">{{page}}</span>
                <span id="topage" style="display:none;">{{topage}}</span>
                
                <!-- Footer content -->
                <div id="footer" class="footer-content">
                    {footer_html}
                </div>
            </body>
            </html>
            """
            
            footer_html_path = tempfile.mktemp(suffix='.html')
            with open(footer_html_path, 'w', encoding='utf-8') as f:
                f.write(footer_html_content)
            temp_files.append(footer_html_path)
        
        # Configure options for wkhtmltopdf
        options = {
            'page-size': 'A4',
            'margin-top': '25mm',
            'margin-right': '15mm',
            'margin-bottom': '25mm',
            'margin-left': '15mm',
            'encoding': 'UTF-8',
            'enable-javascript': None,
            'javascript-delay': 1000,  # Give time for JS to run
            'no-stop-slow-scripts': None,
            'enable-local-file-access': None,
            'quiet': None
        }
        
        # Add header if provided
        if header_html_path:
            options['header-html'] = header_html_path
            options['header-spacing'] = '5'
        
        # Add footer if provided
        if footer_html_path:
            options['footer-html'] = footer_html_path
            options['footer-spacing'] = '5'
            
            # These replace the {{page}} and {{topage}} in the footer HTML
            options['replace'] = [
                ['{{page}}', '[page]'],
                ['{{topage}}', '[topage]']
            ]
        
        # Generate PDF with wkhtmltopdf
        pdfkit.from_file(main_html_path, output_path, options=options, configuration=config)
        
        return output_path
        
    finally:
        # Clean up temporary files
        for path in temp_files:
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass