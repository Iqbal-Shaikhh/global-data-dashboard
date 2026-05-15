import tempfile
import os
from fpdf import FPDF
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Global Data Dashboard Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(title, descriptions, figures, dataframe=None):
    """
    Generates a PDF report.
    :param title: str
    :param descriptions: list of str
    :param figures: list of plotly go.Figure
    :param dataframe: pd.DataFrame (optional)
    :return: bytes
    """
    pdf = PDFReport()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, title, 0, 1, 'L')
    pdf.ln(5)
    
    # Descriptions
    pdf.set_font('Arial', '', 12)
    for desc in descriptions:
        pdf.multi_cell(0, 8, desc)
        pdf.ln(2)
        
    # Figures
    temp_files = []
    try:
        for i, fig in enumerate(figures):
            temp_img_path = tempfile.mktemp(suffix=".png")
            temp_files.append(temp_img_path)
            # Save plotly figure as PNG
            fig.write_image(temp_img_path, format="png", width=800, height=500)
            
            # Add to PDF
            pdf.image(temp_img_path, w=180)
            pdf.ln(5)
            
        # Table (if any)
        if dataframe is not None:
            pdf.set_font('Arial', 'B', 8)
            
            # We need to print headers
            # Reset index to include it in columns if it's meaningful, but for our app it is "Metric"
            df_to_print = dataframe.reset_index()
            columns = [str(c) for c in df_to_print.columns]
            
            # Calculate cell widths simply
            col_width = pdf.w / len(columns) * 0.85
            row_height = pdf.font_size * 2
            
            # Header
            for col in columns:
                pdf.cell(col_width, row_height, col, border=1, align='C')
            pdf.ln(row_height)
            
            # Body
            pdf.set_font('Arial', '', 8)
            for _, row in df_to_print.iterrows():
                for item in row:
                    val_str = str(item)
                    if isinstance(item, float):
                        val_str = f"{item:.2f}"
                    pdf.cell(col_width, row_height, val_str[:40], border=1, align='C')
                pdf.ln(row_height)
    finally:
        # Cleanup temp images
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
                
    # Return as bytes
    return bytes(pdf.output())
