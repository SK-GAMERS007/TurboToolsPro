from fpdf import FPDF

def convert_to_pdf(input_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Converted File:", ln=1)

    pdf_file = "converted.pdf"
    pdf.output(pdf_file)
    return pdf_file
