from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from bs4 import BeautifulSoup
import tempfile
import os

def generate_docx(content_html, header_html, footer_html, output_path, watermark=None):
    """
    Generate a DOCX document from HTML content
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
    
    # Add header if provided
    if header_html:
        header_soup = BeautifulSoup(header_html, 'html.parser')
        for section in doc.sections:
            header = section.header
            header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            header_para.text = header_soup.get_text().strip()
            header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add footer if provided (only on last page for bonus task)
    if footer_html:
        footer_soup = BeautifulSoup(footer_html, 'html.parser')
        
        # Get the last section
        last_section = doc.sections[-1]
        
        # Set up different first page footer
        last_section.different_first_page_header_footer = True
        
        # Add footer to last section
        footer = last_section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.text = footer_soup.get_text().strip()
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add watermark if provided - as a simple text watermark
    if watermark:
        # Get watermark text
        watermark_soup = BeautifulSoup(watermark, 'html.parser') if watermark.strip().startswith('<') else None
        watermark_text = watermark_soup.get_text().strip() if watermark_soup else watermark
        
        # Add simple watermark to every section (page)
        for section in doc.sections:
            # Add the watermark to the header
            hdr = section.header
            # Check if there's already content in the header
            if not hdr.paragraphs:
                hdr_p = hdr.add_paragraph()
            else:
                hdr_p = hdr.paragraphs[0]
            
            # Format paragraph for watermark
            hdr_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Add the watermark text
            watermark_run = hdr_p.add_run(watermark_text.upper())
            watermark_run.font.size = Pt(72)  # Large size
            watermark_run.font.color.rgb = RGBColor(200, 200, 200)  # Light gray
            watermark_run.font.bold = True
    
    # Save the document
    doc.save(output_path)
    return output_path