import json
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Indenter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Example input JSON string (replace this with your actual JSON string)
json_data = '''

[
    {
        "credit_score": "752",
        "dob": "1979-03-21",
        "gender": "male",
        "mobile": "9745522877",
        "name": "JOSHY K G",
        "pan": "AOEPG4524M"
    },
    {
        "Credit Facilities Overview": [
            {
                "Bank": "SBI",
                "Loan Sanctioned (INR)": 800000.0,
                "Loan Type": "Auto Loan (Personal)",
                "Status": "Active"
            },
            {
                "Bank": "HDFC BANK",
                "Loan Sanctioned (INR)": 302592.0,
                "Loan Type": "Credit Card",
                "Status": "Active"
            },
            {
                "Bank": "ICICI BANK",
                "Loan Sanctioned (INR)": 46114.0,
                "Loan Type": "Credit Card",
                "Status": "Active"
            },
            {
                "Bank": "BOB",
                "Loan Sanctioned (INR)": 556000.0,
                "Loan Type": "Gold Loan",
                "Status": "Active"
            },
            {
                "Bank": "MANAPPURAM",
                "Loan Sanctioned (INR)": 309027.0,
                "Loan Type": "Gold Loan",
                "Status": "Active"
            },
            {
                "Bank": "AXIS BANK",
                "Loan Sanctioned (INR)": 2645299.0,
                "Loan Type": "Housing Loan",
                "Status": "Active"
            },
            {
                "Bank": "AVANSE FIN",
                "Loan Sanctioned (INR)": 171100.0,
                "Loan Type": "Personal Loan",
                "Status": "Active"
            },
            {
                "Bank": "AXIS BANK",
                "Loan Sanctioned (INR)": 2000000.0,
                "Loan Type": "Personal Loan",
                "Status": "Active"
            },
            {
                "Bank": "HDFC BANK",
                "Loan Sanctioned (INR)": 464855.0,
                "Loan Type": "Personal Loan",
                "Status": "Active"
            },
            {
                "Bank": "KOTAK BANK",
                "Loan Sanctioned (INR)": 307930.0,
                "Loan Type": "Personal Loan",
                "Status": "Active"
            },
            {
                "Bank": "AXIS BANK",
                "Loan Sanctioned (INR)": 1858341.0,
                "Loan Type": "Property Loan",
                "Status": "Active"
            }
        ]
    },
    {
        "Enquiry Details (Past 6 Months)": [
            {
                "Amount(INR)": "2000000",
                "Date": "2024-09-26",
                "Institution": "AXIS BANK",
                "Purpose": "PERSONAL LOAN"
            },
            {
                "Amount(INR)": "500000",
                "Date": "2024-08-19",
                "Institution": "KOTAK BANK",
                "Purpose": "PERSONAL LOAN"
            },
            {
                "Amount(INR)": "723000",
                "Date": "2024-03-01",
                "Institution": "AXIS BANK",
                "Purpose": "PERSONAL LOAN"
            },
            {
                "Amount(INR)": "600000",
                "Date": "2023-05-02",
                "Institution": "AXIS BANK",
                "Purpose": "PERSONAL LOAN"
            },
            {
                "Amount(INR)": "800000",
                "Date": "2023-04-19",
                "Institution": "SBI",
                "Purpose": "AUTO LOAN"
            },
            {
                "Amount(INR)": "500000",
                "Date": "2023-04-18",
                "Institution": "SBI",
                "Purpose": "AUTO LOAN"
            },
            {
                "Amount(INR)": "2500000",
                "Date": "2023-02-25",
                "Institution": "AXIS BANK",
                "Purpose": "HOUSING LOAN"
            },
            {
                "Amount(INR)": "1500000",
                "Date": "2023-01-18",
                "Institution": "AXIS BANK",
                "Purpose": "PERSONAL LOAN"
            },
            {
                "Amount(INR)": "1000",
                "Date": "2023-01-15",
                "Institution": "RBL BANK LTD",
                "Purpose": "CREDIT CARD"
            },
            {
                "Amount(INR)": "171000",
                "Date": "2023-01-13",
                "Institution": "NDXP",
                "Purpose": "EDUCATIONAL LOAN"
            },
            {
                "Amount(INR)": "2500000",
                "Date": "2022-10-26",
                "Institution": "AXIS BANK",
                "Purpose": "HOUSING LOAN"
            },
            {
                "Amount(INR)": "2500000",
                "Date": "2022-09-06",
                "Institution": "AXIS BANK",
                "Purpose": "HOUSING LOAN"
            },
            {
                "Amount(INR)": "4000000",
                "Date": "2022-05-18",
                "Institution": "AXIS BANK",
                "Purpose": "HOUSING LOAN"
            }
        ]
    },
    {
        "Secured Loans & Collateral Esmate": [
            {
                "Approx Asset Value (Est.)": "617777.78 - 654117.65",
                "Bank": "BOB",
                "Loan Sanctioned (INR)": 556000.0,
                "Loan Type": "Gold Loan",
                "Status": "Active"
            },
            {
                "Approx Asset Value (Est.)": "27777.78 - 29411.76",
                "Bank": "FEDERAL BANK",
                "Loan Sanctioned (INR)": 25000.0,
                "Loan Type": "Gold Loan",
                "Status": "Closed"
            },
            {
                "Approx Asset Value (Est.)": "343363.33 - 363561.18",
                "Bank": "MANAPPURAM",
                "Loan Sanctioned (INR)": 309027.0,
                "Loan Type": "Gold Loan",
                "Status": "Active"
            },
            {
                "Approx Asset Value (Est.)": "14542665.56 - 15398116.47",
                "Bank": "MANAPPURAM",
                "Loan Sanctioned (INR)": 13088399.0,
                "Loan Type": "Gold Loan",
                "Status": "Closed"
            },
            {
                "Approx Asset Value (Est.)": "2939221.11 - 3112116.47",
                "Bank": "AXIS BANK",
                "Loan Sanctioned (INR)": 2645299.0,
                "Loan Type": "Housing Loan",
                "Status": "Active"
            },
            {
                "Approx Asset Value (Est.)": "894444.44 - 947058.82",
                "Bank": "FEDERAL BANK",
                "Loan Sanctioned (INR)": 805000.0,
                "Loan Type": "Housing Loan",
                "Status": "Closed"
            },
            {
                "Approx Asset Value (Est.)": "2064823.33 - 2186283.53",
                "Bank": "AXIS BANK",
                "Loan Sanctioned (INR)": 1858341.0,
                "Loan Type": "Property Loan",
                "Status": "Active"
            }
        ]
    },
    {
        "Closed Loan Accounts": [
            {
                "Bank": "PNB",
                "Loan Sanctioned (INR)": 950000.0,
                "Loan Type": "Auto Loan (Personal)",
                "Status": "Closed"
            },
            {
                "Bank": "CANARA BANK",
                "Loan Sanctioned (INR)": 346000.0,
                "Loan Type": "Business Loan – Priority Sector – Agriculture",
                "Status": "Closed"
            },
            {
                "Bank": "BAJAJ FIN LTD",
                "Loan Sanctioned (INR)": 167469.0,
                "Loan Type": "Consumer Loan",
                "Status": "Closed"
            },
            {
                "Bank": "CITICORP FINANCE",
                "Loan Sanctioned (INR)": 29000.0,
                "Loan Type": "Consumer Loan",
                "Status": "Closed"
            },
            {
                "Bank": "FEDERAL BANK",
                "Loan Sanctioned (INR)": 25000.0,
                "Loan Type": "Gold Loan",
                "Status": "Closed"
            },
            {
                "Bank": "MANAPPURAM",
                "Loan Sanctioned (INR)": 13088399.0,
                "Loan Type": "Gold Loan",
                "Status": "Closed"
            },
            {
                "Bank": "FEDERAL BANK",
                "Loan Sanctioned (INR)": 805000.0,
                "Loan Type": "Housing Loan",
                "Status": "Closed"
            },
            {
                "Bank": "AXIS BANK",
                "Loan Sanctioned (INR)": 11000000.0,
                "Loan Type": "Personal Loan",
                "Status": "Closed"
            },
            {
                "Bank": "CITICORP FINANCE",
                "Loan Sanctioned (INR)": 74800.0,
                "Loan Type": "Personal Loan",
                "Status": "Closed"
            },
            {
                "Bank": "FEDERAL BANK",
                "Loan Sanctioned (INR)": 70000.0,
                "Loan Type": "Personal Loan",
                "Status": "Closed"
            },
            {
                "Bank": "HDFC BANK",
                "Loan Sanctioned (INR)": 301972.0,
                "Loan Type": "Personal Loan",
                "Status": "Closed"
            },
            {
                "Bank": "KOTAK BANK",
                "Loan Sanctioned (INR)": 201862.0,
                "Loan Type": "Personal Loan",
                "Status": "Closed"
            },
            {
                "Bank": "MANAPPURAM",
                "Loan Sanctioned (INR)": 610.0,
                "Loan Type": "Personal Loan",
                "Status": "Closed"
            },
            {
                "Bank": "BAJAJ FIN LTD",
                "Loan Sanctioned (INR)": 33800.0,
                "Loan Type": "Two wheeler Loan",
                "Status": "Closed"
            }
        ]
    },
    {
        "Loan Appraisal Scorecard": [
            {
                "Metric": "CIBIL Score",
                "Value": 20.89
            },
            {
                "Metric": "Repayment History",
                "Value": 15.0
            },
            {
                "Metric": "Enquiry Frequency",
                "Value": 4.0
            },
            {
                "Metric": "Credit Mix",
                "Value": 10.0
            },
            {
                "Metric": "Has Secured Loan",
                "Value": 10.0
            }
        ]
    }
]
'''
data = json.loads(json_data)
# personal_info = dict_list[0]


# # Initialize styles
# styles = getSampleStyleSheet()
# normal_style = styles['Normal']

# header_style = ParagraphStyle(
#     name='HeaderStyle',
#     fontName='Helvetica-Bold',
#     fontSize=9,
#     alignment=TA_CENTER,
#     textColor=colors.white
# )

# cell_style = ParagraphStyle(
#     name='CellStyle',
#     fontName='Helvetica',
#     fontSize=9,
#     alignment=TA_CENTER
# )

# label_style = ParagraphStyle(
#     name='LabelStyle',
#     fontName='Helvetica-Bold',
#     fontSize=10,
#     alignment=TA_LEFT
# )

# value_style = ParagraphStyle(
#     name='ValueStyle',
#     fontName='Helvetica',
#     fontSize=10,
#     alignment=TA_LEFT
# )


# # Function to create styled table from dict list
# def create_table_from_dict_list(dict_list, col_widths=None):
#     if not dict_list:
#         return Paragraph("No data available", normal_style)

#     headers = list(dict_list[0].keys())
#     table_data = [[Paragraph(h, header_style) for h in headers]]

#     for entry in dict_list:
#         row = [Paragraph(str(entry.get(h, "")), cell_style) for h in headers]
#         table_data.append(row)

#     table = Table(table_data, colWidths=col_widths, hAlign='LEFT')
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 0), (-1, -1), 9),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('LEFTPADDING', (0, 0), (-1, -1), 4),
#         ('RIGHTPADDING', (0, 0), (-1, -1), 4),
#         ('TOPPADDING', (0, 0), (-1, -1), 3),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
#     ]))
#     return table

# # Function to create personal info table
# def create_personal_info_table(info_dict):
#     data = []
#     for key, val in info_dict.items():
#         data.append([
#             Paragraph(f"{key}", label_style),
#             Paragraph(str(val), value_style)
#         ])
#     table = Table(data, colWidths=[1.5 * inch, 4.5 * inch])
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),
#         ('LEFTPADDING', (0, 0), (-1, -1), 4),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
#     ]))
#     return table

# # Main PDF generator
# def generate_pdf(filename):
#     doc = SimpleDocTemplate(filename, pagesize=A4)
#     elements = []

#     elements.append(Paragraph("<b>Personal Details</b>", styles['Heading2']))
#     elements.append(Spacer(1, 6))
#     elements.append(create_personal_info_table(personal_info))
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph("<b>Credit Facilities Overview</b>", styles['Heading2']))
#     elements.append(Spacer(1, 6))
#     table = create_table_from_dict_list(dict_list[1], col_widths=[1.5*inch, 1.5*inch, 2*inch, 1.2*inch])
#     elements.append(table)

#     doc.build(elements)

# # Call function
# generate_pdf("credit_report.pdf")


################################## next code ##################################################################


# Output PDF file
output_file = "credit_report.pdf"

# PDF Setup
doc = SimpleDocTemplate(output_file, pagesize=A4)
elements = []
styles = getSampleStyleSheet()
title_style = styles['Heading1']
section_style = styles['Heading2']
normal_style = styles['Normal']

def add_title(title):
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(title, section_style))
    elements.append(Spacer(1, 6))

def create_table_from_dict_list(dict_list):
    if not dict_list:
        return Paragraph("No data available", normal_style)
    headers = dict_list[0].keys()
    table_data = [list(headers)]
    for entry in dict_list:
        table_data.append([str(entry.get(h, "")) for h in headers])
    table = Table(table_data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))
    return table

# 1. Personal Info
elements.append(Paragraph("Credit Report", title_style))
elements.append(Spacer(1, 12))
personal_info = data[0]
add_title("Personal Information")
for key, value in personal_info.items():
    elements.append(Paragraph(f"<b>{key}:</b> {value}", normal_style))
elements.append(Spacer(1, 12))

# 2. Credit Facilities
credit_facilities = next((section.get("Credit Facilities Overview") for section in data if "Credit Facilities Overview" in section), [])
add_title("Credit Facilities Overview")
elements.append(create_table_from_dict_list(credit_facilities))

# 3. Enquiries
enquiries = next((section.get("Enquiry Details (Past 6 Months)") for section in data if "Enquiry Details (Past 6 Months)" in section), [])
add_title("Enquiry Details")
elements.append(create_table_from_dict_list(enquiries))

# 4. Secured Loans
secured_loans = next((section.get("Secured Loans & Collateral Esmate") for section in data if "Secured Loans & Collateral Esmate" in section), [])
add_title("Secured Loans & Collateral Esmate")
elements.append(create_table_from_dict_list(secured_loans))

# 5. Closed Loans
closed_loans = next((section.get("Closed Loan Accounts") for section in data if "Closed Loan Accounts" in section), [])
add_title("Closed Loan Accounts")
elements.append(create_table_from_dict_list(closed_loans))

# 5. Closed Loans
closed_loans = next((section.get("Loan Appraisal Scorecard") for section in data if "Loan Appraisal Scorecard" in section), [])
add_title("Loan Appraisal Scorecard")
elements.append(create_table_from_dict_list(closed_loans))

# Generate the PDF
doc.build(elements)
print(f"PDF saved to: {output_file}")