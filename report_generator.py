import tempfile
import os
from fpdf import FPDF
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        # Add colored background for header
        self.set_fill_color(41, 128, 185)  # Blue background
        self.set_text_color(255, 255, 255)  # White text
        self.set_font('Arial', 'B', 15)
        self.cell(0, 15, 'Global Data Dashboard Report', 0, 1, 'C', fill=True)
        self.set_text_color(0, 0, 0)  # Reset to black
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)  # Gray text
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        self.set_text_color(0, 0, 0)  # Reset to black

def generate_pdf(title, descriptions, figures, dataframe=None):
    """
    Generates a PDF report with color styling.
    :param title: str
    :param descriptions: list of str
    :param figures: list of plotly go.Figure
    :param dataframe: pd.DataFrame (optional)
    :return: bytes
    """
    pdf = PDFReport()
    pdf.add_page()
    
    # Title with accent color
    pdf.set_fill_color(52, 152, 219)  # Lighter blue
    pdf.set_text_color(255, 255, 255)  # White text
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, title, 0, 1, 'L', fill=True)
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(3)
    
    # Descriptions with styled text
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(50, 50, 50)  # Dark gray
    for desc in descriptions:
        pdf.multi_cell(0, 6, desc)
        pdf.ln(1)
    
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(2)
        
    # Figures
    temp_files = []
    try:
        for i, fig in enumerate(figures):
            temp_img_path = tempfile.mktemp(suffix=".png")
            temp_files.append(temp_img_path)
            # Save plotly figure as PNG
            fig.write_image(temp_img_path, format="png", width=800, height=500)
            
            # Add figure separator line with color
            pdf.set_draw_color(200, 200, 200)  # Light gray line
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
            
            # Add to PDF
            pdf.image(temp_img_path, w=180)
            pdf.ln(2)
            
        # Table (if any)
        if dataframe is not None:
            pdf.ln(3)
            
            # Table title
            pdf.set_fill_color(52, 152, 219)  # Blue background
            pdf.set_text_color(255, 255, 255)  # White text
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 10, 'Data Table', 0, 1, 'L', fill=True)
            pdf.set_text_color(0, 0, 0)  # Reset to black
            pdf.ln(2)
            
            # Reset index to include it in columns if it's meaningful, but for our app it is "Metric"
            df_to_print = dataframe.reset_index()
            columns = [str(c) for c in df_to_print.columns]
            
            # Calculate cell widths simply
            col_width = pdf.w / len(columns) * 0.85
            row_height = pdf.font_size * 2.5
            
            # Header with color
            pdf.set_fill_color(41, 128, 185)  # Darker blue
            pdf.set_text_color(255, 255, 255)  # White text
            pdf.set_font('Arial', 'B', 9)
            for col in columns:
                pdf.cell(col_width, row_height, col, border=1, align='C', fill=True)
            pdf.ln(row_height)
            pdf.set_text_color(0, 0, 0)  # Reset to black
            
            # Body with alternating row colors
            pdf.set_font('Arial', '', 8)
            for row_idx, (_, row) in enumerate(df_to_print.iterrows()):
                # Alternate row colors
                if row_idx % 2 == 0:
                    pdf.set_fill_color(245, 245, 245)  # Light gray
                else:
                    pdf.set_fill_color(255, 255, 255)  # White
                
                for item in row:
                    val_str = str(item)
                    if isinstance(item, float):
                        val_str = f"{item:.2f}"
                    pdf.cell(col_width, row_height, val_str[:40], border=1, align='C', fill=True)
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
