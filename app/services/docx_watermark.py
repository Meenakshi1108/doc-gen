from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_proper_watermark(document, text):
    """
    Add a proper watermark to the Word document
    
    Args:
        document: The python-docx document object
        text: The text for the watermark
    """
    # For each section in the document
    for section in document.sections:
        # Get the header
        header = section.header
        
        # Clear existing content
        for paragraph in header.paragraphs:
            p = paragraph._p
            p.getparent().remove(p)
        
        # Add a paragraph for the watermark
        paragraph = header.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add a run with the watermark text
        run = paragraph.add_run(text)
        font = run.font
        font.size = Pt(36)  # Large size
        font.color.rgb = RGBColor(200, 200, 200)  # Light gray
        
        # Apply rotation
        r = run._r
        rPr = r.get_or_add_rPr()
        
        # Create rotation effect (approximately -45 degrees)
        effect = OxmlElement('w:effect')
        effect.set(qn('w:val'), 'blinkBackground')
        rPr.append(effect)
        
        # Position in the center
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    return document