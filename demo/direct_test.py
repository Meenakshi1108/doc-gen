import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import generate_document

def test_watermark():
    """Test document generation with proper watermark"""
    
    # Create output directory if it doesn't exist
    os.makedirs("demo/output", exist_ok=True)
    
    # Sample HTML content
    content_html = """
    <h1 style="color: #333; text-align: center;">Confidential Report</h1>
    <p style="margin: 15px 0;">This document contains watermarked content to demonstrate proper watermark implementation.</p>
    <h2>Important Information</h2>
    <ul>
        <li>The watermark should appear behind this content</li>
        <li>It should be visible on all pages</li>
        <li>It should not be easily removable</li>
    </ul>
    <p>Let's add more content to potentially create multiple pages:</p>
    <table border="1" cellpadding="5" style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #f2f2f2;">
            <th>Item</th>
            <th>Description</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Item 1</td>
            <td>First important item</td>
            <td>$1,000</td>
        </tr>
        <tr>
            <td>Item 2</td>
            <td>Second important item</td>
            <td>$2,500</td>
        </tr>
    </table>
    <h2>Section 2</h2>
    <p>More content to demonstrate the watermark appears on all pages consistently.</p>
    <p>The watermark should be subtle enough to not interfere with reading the document.</p>
    """

    header_html = """
    <div style="text-align: center; font-size: 10px; color: #777;">
        ACME Corporation - Confidential Document
    </div>
    """
    
    footer_html = """
    <div style="text-align: center; font-size: 10px; color: #777;">
        Page 1 - Generated on 2025-03-25 07:40:49
    </div>
    """
    
    watermark = "CONFIDENTIAL"  # Plain text watermark
    
    # Test PDF watermark
    print("Testing PDF watermark...")
    pdf_output_path = "demo/output/watermarked.pdf"
    
    try:
        generate_document(
            content_html=content_html,
            header_html=header_html,
            footer_html=footer_html,
            document_type="pdf",
            output_path=pdf_output_path,
            watermark=watermark
        )
        print(f"PDF with watermark generated at {pdf_output_path}")
    except Exception as e:
        print(f"PDF generation failed: {str(e)}")
    
    # Test DOCX watermark
    print("Testing DOCX watermark...")
    docx_output_path = "demo/output/watermarked.docx"
    
    try:
        generate_document(
            content_html=content_html,
            header_html=header_html,
            footer_html=footer_html,
            document_type="docx",
            output_path=docx_output_path,
            watermark=watermark
        )
        print(f"DOCX with watermark generated at {docx_output_path}")
    except Exception as e:
        print(f"DOCX generation failed: {str(e)}")

if __name__ == "__main__":
    test_watermark()