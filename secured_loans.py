import datetime as dt
import pandas as pd
import json
from flask import jsonify

#------------------------------------------- READ DATA --------------------------------------

# with open(r"D:\11_August_Chatbot_Faiss_Env\BSA_Advance\BSA (2)\Credit_Report_Remote_Repository\credit-report\joshykg-credit-report.json",'r') as file:
#     data = json.load(file)

def secured_loans(data):
    #----------------------------------------- FIND ALL LOANS ---------------------------------------

    try:
        loans = data["data"]["credit_report"][0]["accounts"]
        loans_list = []
        if loans:
            for loan in loans:
                loans_info = {}
                loans_info["Loan Type"] = loan["accountType"]
                loans_info["Bank"] = loan["memberShortName"]
                loans_info["Loan Sanctioned (INR)"] = loan["highCreditAmount"]
                # loans_info["Current Balance (INR)"] = loan["currentBalance"]
                loans_info["Status"] = loan["dateClosed"]
                loans_list.append(loans_info)

        df_loan = pd.DataFrame(loans_list)
        df_loan["Loan Sanctioned (INR)"] = df_loan["Loan Sanctioned (INR)"].astype(float)

    except Exception as e:
        return jsonify({"error": "Error processing loans table in secured loans section", "details": str(e)}), 500

    #----------------------------------------- FIND STATUS OF ALL LOANS AND CREATE GROUPS ---------------------------------------

    try:
        # Check status 
        status = []
        for st in df_loan["Status"].to_list():
            if st:
                if st == "NA":
                    status.append("Active")
                else:
                    status.append("Closed")

        df_loan["Status"] = status

        # print(sum(df_loan[df_loan["Loan Type"] == "Property Loan"]["Loan Sanctioned (INR)"].to_list()))

        # group by loan types, banks and Status
        grouped_loans = df_loan.groupby(["Loan Type","Bank","Status"]).sum()
        df = grouped_loans.reset_index()
        df_dict = df.to_dict(orient="records")
        
    except Exception as e:
        return jsonify({"error": "Error processing status or group by table secured loans section", "details": str(e)}), 500
    
    #----------------------------- CALCULATE SECURED LOANS AND COLLATERAL ----------------------------------

    try:
        df_secured_loans = df[df["Loan Type"].isin(["Gold Loan","Property Loan","Housing Loan","Auto Loan"])].copy()

        asset_values = []
        for loan_value in df_secured_loans["Loan Sanctioned (INR)"].to_list():
            if loan_value:
                upper_asset_value = round((int(loan_value) / 0.85 ), 2)
                lower_asset_value = round((int(loan_value) / 0.90), 2)
                asset_value = f"{lower_asset_value} - {upper_asset_value}"
                asset_values.append(asset_value)
        
        df_secured_loans["Approx Asset Value (Est.)"] = asset_values

        df_secured_loans_dictionary = df_secured_loans.to_dict(orient="records")
        
        return [df_dict,df_secured_loans_dictionary]
    
    except Exception as e:
        return jsonify({"error": "Error calculating secured loans and collateral in secured loans section", "details": str(e)}), 500