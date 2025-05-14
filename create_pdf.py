import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import tempfile
import os

def df_to_image(df, filename):
    fig, ax = plt.subplots(figsize=(len(df.columns)*1.5, len(df)*0.5 + 1))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    fig.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close(fig)

def create_pdf_with_dataframes(
    df_info_list,  # List of tuples: (title, df, description)
    output_path='output.pdf'
):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    for title, df, description in df_info_list:
        # Add title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, title)

        # Add description (if any)
        if description:
            c.setFont("Helvetica", 10)
            text = c.beginText(50, height - 70)
            for line in description.split('\n'):
                text.textLine(line)
            c.drawText(text)

        # Add dataframe as image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            df_to_image(df, tmp.name)
            img = ImageReader(tmp.name)
            c.drawImage(img, 50, 100, width=500, preserveAspectRatio=True, mask='auto')
            c.showPage()
            os.unlink(tmp.name)

    c.save()
    print(f"PDF saved to: {r'./credit-report/'}")

