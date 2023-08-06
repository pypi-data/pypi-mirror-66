from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime


def drawMyRuler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')


def generate_report(file_name):

    title = "Congruous Match Report"

    pdf = canvas.Canvas(file_name)
    pdf.setTitle(title)
    drawMyRuler(pdf)

    # Set Logo
    image = 'logo.png'
    pdf.drawInlineImage(image, 40, 720)

    # Register font
    pdfmetrics.registerFont(
        TTFont('abc', 'OpenSans-Bold.ttf')
    )

    # Center the title and write
    pdf.setFont("abc", 24)
    pdf.drawCentredString(320, 750, title)

    # Draw a line below the title
    pdf.line(50, 730, 500, 730)

    # Set the date
    report_date = "Date: " + datetime.now().strftime("%d/%m/%Y")
    pdfmetrics.registerFont(
        TTFont('abc', 'OpenSans-Regular.ttf')
    )
    pdf.setFont("abc", 12)
    report = pdf.beginText(450, 680)
    report.textOut(report_date)
    pdf.drawText(report)

    # Set the report Id
    report_id = "Report no.: #8058900"
    pdfmetrics.registerFont(
        TTFont('abc', 'OpenSans-Regular.ttf')
    )

    pdf.setFont('abc', 12)
    report = pdf.beginText(50, 680)
    report.textOut(report_id)
    pdf.drawText(report)

    report_description = "The following pie-charts depicts the match percentage of custom-built OCR parsed data with its human curated data."
    pdfmetrics.registerFont(
        TTFont('abc', 'OpenSans-Light.ttf')
    )

    pdf.setFont('abc', 9)
    report = pdf.beginText(50, 630)
    report.textOut(report_description)
    pdf.drawText(report)

    # Set other field values
    # Set piechart

    pdf.save()


generate_report("12345.pdf")
