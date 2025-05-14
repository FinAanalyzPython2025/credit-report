import json
import pandas as pd
from flask import jsonify
import traceback

def map_enquiry_purpose(df):
    ACCOUNT_TYPE = {
        "1": "AUTO LOAN", "2": "HOUSING LOAN", "3": "PROPERTY LOAN", "4": "LOAN AGAINST SHARES/SECURITIES",
        "5": "PERSONAL LOAN", "6": "CONSUMER LOAN", "7": "GOLD LOAN", "8": "EDUCATIONAL LOAN",
        "9": "LOAN TO PROFESSIONAL", "10": "CREDIT CARD", "11": "LEASING", "12": "OVERDRAFT",
        "13": "TWO-WHEELER LOAN", "14": "NON-FUNDED CREDIT FACILITY", "15": "LOAN AGAINST BANK DEPOSITS",
        "16": "FLEET CARD", "17": "Commercial Vehicle Loan", "18": "Telco - Wireless", "19": "Telco - Broadband",
        "20": "Telco - Landline", "23": "GECL Secured", "24": "GECL Unsecured", "31": "Secured Credit Card",
        "32": "Used Car Loan", "33": "Construction Equipment Loan", "34": "Tractor Loan",
        "35": "Corporate Credit Card", "36": "Kisan Credit Card", "37": "Loan on Credit Card",
        "38": "PM Jaan Dhan Yojana - Overdraft", "39": "Mudra Loans", "40": "Microfinance - Business Loan",
        "41": "Microfinance - Personal Loan", "42": "Microfinance - Housing Loan", "43": "Microfinance - Others",
        "44": "PM Awas Yojana - CLSS", "45": "P2P Personal Loan", "46": "P2P Auto Loan", "47": "P2P Education Loan",
        "50": "Business Loan - Secured", "51": "Business Loan - General", "52": "Priority Sector - Small Business",
        "53": "Priority Sector - Agriculture", "54": "Priority Sector - Others",
        "55": "Business Non-Funded Credit Facility - General", "56": "Priority Sector - Small Business",
        "57": "Priority Sector - Agriculture", "58": "Priority Sector - Others",
        "59": "Business Loan Against Bank Deposits", "60": "Staff Loan", "61": "Business Loan - Unsecured",
        "69": "Short Term Personal Loan", "70": "Priority Sector Gold Loan", "71": "Temporary Overdraft",
        "blank": "", "00": "Others", "": ""
    }

    # Strip leading zeros before mapping
    df['enquiryPurpose'] = df['enquiryPurpose'].astype(str).str.lstrip('0').apply(lambda x: ACCOUNT_TYPE.get(x, x))
    return df

def extract_enquiry_data(json_data):
    try:
        enquiries = json_data['data']['credit_report'][0].get('enquiries', [])
        df = pd.DataFrame(enquiries)

        if 'index' in df.columns:
            df.drop('index', axis=1, inplace=True)

        # Map purposes first
        if 'enquiryPurpose' in df.columns:
            df = map_enquiry_purpose(df)
        else:
            raise KeyError("Missing 'enquiryPurpose' column in data")

        # Then rename and reorder
        df = df.rename(columns={
            'enquiryDate': 'Date',
            'memberShortName': 'Institution',
            'enquiryPurpose': 'Purpose',
            'enquiryAmount': 'Amount(INR)'
        })

        df = df[['Date', 'Institution', 'Purpose', 'Amount(INR)']]
        # print("Mapped and Reordered DataFrame:\n", df)

<<<<<<< HEAD
        return df

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Error processing enquiries section", "details": str(e)}), 500
=======
        enq_dict = df.to_dict(orient="records")

        return enq_dict

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Error processing enquiries section", "details": str(e)}), 500
>>>>>>> 53328b068d34b9a179d687a76f3ba40e66eb1680
