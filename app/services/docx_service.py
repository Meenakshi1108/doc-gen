from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from bs4 import BeautifulSoup
import os

def generate_docx(content_html, header_html, footer_html, output_path, watermark=None):
    """
    Generate a DOCX document from HTML content
    Improved version that correctly handles:
    - Watermark on all pages
    - Footer only on the last page
    """
    # Create a new Document
    doc = Document()
    
    # Set document properties for better formatting
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)
    
    # Parse the content HTML
    soup = BeautifulSoup(content_html, 'html.parser')
    
    # Process each HTML element and add to document
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'table']):
        if element.name == 'h1':
            heading = doc.add_heading(element.get_text().strip(), level=1)
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif element.name == 'h2':
            heading = doc.add_heading(element.get_text().strip(), level=2)
        elif element.name == 'h3':
            heading = doc.add_heading(element.get_text().strip(), level=3)
        elif element.name == 'p':
            para = doc.add_paragraph(element.get_text().strip())
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li'):
                para = doc.add_paragraph(li.get_text().strip())
                para.style = 'List Bullet' if element.name == 'ul' else 'List Number'
        elif element.name == 'table':
            # Create a table with the right number of rows and columns
            rows = element.find_all('tr')
            if rows:
                cols = max(len(row.find_all(['td', 'th'])) for row in rows)
                table = doc.add_table(rows=len(rows), cols=cols)
                table.style = 'Table Grid'
                
                # Fill the table with data
                for i, row in enumerate(rows):
                    cells = row.find_all(['td', 'th'])
                    for j, cell in enumerate(cells):
                        if j < cols:  # Safety check
                            table.cell(i, j).text = cell.get_text().strip()
    
    # Create a section break for the last page
    doc.add_section(WD_SECTION.NEW_PAGE)
    
    # Add a simple paragraph to the last page
    last_para = doc.add_paragraph("End of Document")
    last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add header if provided
    if header_html:
        header_soup = BeautifulSoup(header_html, 'html.parser')
        header_text = header_soup.get_text().strip()
        
        for section in doc.sections:
            header = section.header
            if not header.paragraphs:
                header_para = header.add_paragraph()
            else:
                header_para = header.paragraphs[0]
            header_para.text = header_text
            header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add watermark to all pages
    if watermark:
        watermark_text = watermark
        if watermark.startswith('<'):
            # Extract text from HTML
            watermark_soup = BeautifulSoup(watermark, 'html.parser')
            watermark_text = watermark_soup.get_text().strip()
        
        # Apply watermark to all sections
        for section in doc.sections:
            add_watermark(section, watermark_text.upper())
    
    # Add footer only to the last section
    if footer_html:
        footer_soup = BeautifulSoup(footer_html, 'html.parser')
        footer_text = footer_soup.get_text().strip()
        
        # Get the last section
        last_section = doc.sections[-1]
        
        # Make sure footer doesn't appear on other sections
        for i, section in enumerate(doc.sections):
            if i < len(doc.sections) - 1:
                section.footer.is_linked_to_previous = False
                if section.footer.paragraphs:
                    section.footer.paragraphs[0].text = ""
        
        # Add footer to the last section only
        last_section.footer.is_linked_to_previous = False
        if not last_section.footer.paragraphs:
            footer_para = last_section.footer.add_paragraph()
        else:
            footer_para = last_section.footer.paragraphs[0]
        
        footer_para.text = footer_text + " (Last Page Only)"
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Save the document
    doc.save(output_path)
    return output_path

def add_watermark(section, text):
    """Add a watermark to a section"""
    # Get the header part
    header_part = section.header._element
    
    # Check if the watermark already exists
    for child in header_part.iterchildren():
        if child.tag.endswith('p'):
            for grandchild in child.iterchildren():
                if grandchild.tag.endswith('r'):
                    return  # Watermark already exists
    
    # Create paragraph for watermark
    watermark_para = section.header.add_paragraph()
    watermark_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add the watermark text with formatting
    run = watermark_para.add_run(text)
    run.font.size = Pt(72)  # Large size
    run.font.bold = True
    run.font.color.rgb = RGBColor(191, 191, 191)  # Light gray
    
    # Get the XML element for the paragraph
    p = watermark_para._p
    
    # Add vanish property to paragraph properties to make it behind text
    pPr = p.get_or_add_pPr()
    
    # Add watermark effect
    try:
        rPr = run._r.get_or_add_rPr()
        effect = OxmlElement('w:effect')
        effect.set(qn('w:val'), 'shadow')
        rPr.append(effect)
    except:
        pass
    
    return watermark_para