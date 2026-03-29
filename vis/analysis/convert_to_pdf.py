from fpdf import FPDF, XPos, YPos
import markdown
import re
import os

class PDFReport(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_markdown_table(self, header, rows):
        self.set_font('helvetica', 'B', 10)
        with self.table(
            borders_layout="HORIZONTAL_LINES",
            cell_fill_color=245,
            cell_fill_mode="ROWS",
            line_height=8,
            text_align=("LEFT", "CENTER", "CENTER", "CENTER"),
            width=self.epw,
        ) as table:
            row = table.row()
            for item in header:
                row.cell(item)
            self.set_font('helvetica', '', 10)
            for r in rows:
                row = table.row()
                for item in r:
                    row.cell(item)
        self.ln(5)

def parse_and_generate_pdf(md_file, pdf_file):
    pdf = PDFReport()
    pdf.add_page()
    
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Pre-process content to handle images specifically if needed, 
    # but write_html handles <img>.
    # We just need to make sure relative paths work.
    
    # Split by tables
    parts = re.split(r'(\n\|.*\|\n(?:\|.*\|\n)+)', content)
    
    for part in parts:
        part = part.strip()
        if not part: continue
        
        if part.startswith('|'): # Table detected
            lines = [l for l in part.split('\n') if l.strip()]
            header = [h.strip() for h in lines[0].split('|') if h.strip()]
            rows = []
            for l in lines:
                if '|' in l and '--' not in l:
                    row_data = [c.strip() for c in l.split('|') if c.strip()]
                    if row_data != header:
                        rows.append(row_data)
            pdf.add_markdown_table(header, rows)
        else:
            # Handle images manually to ensure they are centered and sized well
            # markdown.markdown converts ![alt](img.png) to <p><img alt="alt" src="img.png" /></p>
            
            # Let's split this part further by images to have better control
            subparts = re.split(r'(!\[.*?\]\(.*?\))', part)
            for sub in subparts:
                sub = sub.strip()
                if not sub: continue
                
                if sub.startswith('!['):
                    # Extract path: ![alt](path)
                    img_path = re.search(r'\((.*?)\)', sub).group(1)
                    if os.path.exists(img_path):
                        # Center the image
                        pdf.image(img_path, x=20, w=pdf.epw - 40)
                        pdf.ln(5)
                else:
                    html = markdown.markdown(sub)
                    pdf.set_font('helvetica', '', 11)
                    pdf.write_html(html)
                    pdf.ln(2)

    pdf.output(pdf_file)

if __name__ == "__main__":
    parse_and_generate_pdf('earnings_report_california_2014.md', 'earnings_report_california_2014.pdf')
    print("PDF generated with graphs: earnings_report_california_2014.pdf")
