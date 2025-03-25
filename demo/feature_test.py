import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import generate_document
import datetime

def test_document_features():
    """
    Test specific document generation features:
    1. Watermark positioned properly and appearing on all pages
    2. Footer appearing only on the last page
    3. No duplicate page numbers
    """
    # Create output directory if it doesn't exist
    os.makedirs("demo/output", exist_ok=True)
    
    # Get current time for the document
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a multi-page document with plenty of content
    html_content = f"""
    <h1 style="color: #333; text-align: center;">Document Feature Test</h1>
    <p><strong>Generated at:</strong> {now} UTC</p>
    <p>This document tests two specific features:</p>
    <ol>
        <li>Watermarks should appear on <strong>all pages</strong> and be properly centered</li>
        <li>Footer should appear <strong>only on the last page</strong></li>
    </ol>
    
    <h2>Page 1 Content</h2>
    <p>This is page 1 content. The watermark should be visible behind this text.</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    
    <table border="1" cellpadding="5" style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #f2f2f2;">
            <th>Feature</th>
            <th>Expected Behavior</th>
        </tr>
        <tr>
            <td>Watermark</td>
            <td>Should appear centered on <strong>every page</strong></td>
        </tr>
        <tr>
            <td>Footer</td>
            <td>Should appear <strong>only on the last page</strong></td>
        </tr>
    </table>
    
    <p style="page-break-before: always;"></p>
    <h2>Page 2 Content</h2>
    <p>This is page 2 content. The watermark should also be visible on this page.</p>
    <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
    <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>
    
    <p style="page-break-before: always;"></p>
    <h2>Page 3 Content</h2>
    <p>This is page 3 content. The watermark should be visible here as well.</p>
    <p>Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.</p>
    <p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>
    
    <h2>Last Page Check</h2>
    <p>This is the final content of the document. The footer should appear below this text, but <strong>only on this last page</strong>.</p>
    <p>If implemented correctly:</p>
    <ul>
        <li>The "CONFIDENTIAL" watermark should appear on all pages</li>
        <li>The footer saying "This footer should only appear on the last page" should only appear here</li>
        <li>No duplicate page numbering should be visible anywhere</li>
    </ul>
    """
    
    header_html = """
    <div style="text-align: center; font-size: 10px; color: #777;">
        Document Feature Test - Watermark and Conditional Footer Demo
    </div>
    """
    
    footer_html = """
    <div style="text-align: center; border-top: 1px solid #cccccc; padding-top: 10px;">
        <strong>This footer should only appear on the last page</strong>
    </div>
    """
    
    watermark = "CONFIDENTIAL"
    
    # Test both PDF and DOCX formats
    print("\nTesting PDF document features...")
    pdf_path = "demo/output/feature_test.pdf"
    
    try:
        generate_document(
            content_html=html_content,
            header_html=header_html,
            footer_html=footer_html,
            document_type="pdf",
            output_path=pdf_path,
            watermark=watermark
        )
        print(f"✓ PDF generated successfully at: {pdf_path}")
    except Exception as e:
        print(f"✗ PDF generation failed: {str(e)}")
        
    print("\nTesting DOCX document features...")
    docx_path = "demo/output/feature_test.docx"
    
    try:
        generate_document(
            content_html=html_content,
            header_html=header_html,
            footer_html=footer_html,
            document_type="docx",
            output_path=docx_path,
            watermark=watermark
        )
        print(f"✓ DOCX generated successfully at: {docx_path}")
    except Exception as e:
        print(f"✗ DOCX generation failed: {str(e)}")
        
    print("\nPlease check the generated documents to verify:")
    print("1. The watermark appears centered on all pages")
    print("2. The footer appears only on the last page")
    print("3. No duplicate page numbers are visible")

if __name__ == "__main__":
    test_document_features()