import datetime as dt
import pandas as pd
import json
from flask import jsonify

#------------------------------------------- READ DATA --------------------------------------

# with open(r'D:\LiteFin\12_LOS\credit report\joshykg-credit-report.json','r') as file:
#     data = json.load(file)

def loan_appraisal_scorecard(data):
    #----------------------------------------- FIND ALL LOANS ---------------------------------------

 
    loans = data["data"]["credit_report"][0]["accounts"]
    loans_list = []
    if loans:
        for loan in loans:
            loans_info = {}
            loans_info["Loan Type"] = loan["accountType"]
            loans_info["Bank"] = loan["memberShortName"]
            loans_info["Loan Sanctioned (INR)"] = loan["highCreditAmount"]
            loans_info["Current Balance"] = loan["currentBalance"]
            loans_info["Status"] = loan["dateClosed"]
            loans_info["Payment History"] = loan["paymentHistory"]
            loans_list.append(loans_info)

    df_loan = pd.DataFrame(loans_list)
    df_loan["Loan Sanctioned (INR)"] = df_loan["Loan Sanctioned (INR)"].astype(float)
    
    # --------------------------------------------- LOAN APPRAISAL SCORECARD --------------------------------------
    
    scorecard = {}
    cibil_score_weight = float(int(data["data"]["credit_score"]) / 900 ) * 25
    scorecard['CIBIL Score'] = round(cibil_score_weight,2)

    payment_history = ''.join(df_loan['Payment History'].to_list())

    def is_valid_grouped_string(s):
        # Group the string in chunks of 3
        groups = [s[i:i+3] for i in range(0, len(s), 3)]

        count = 0
        # Check each group
        for group in groups:
            if group not in ('000', 'xxx', 'STD', 'XXX'):
                if 15 > float(group) > 7 :
                    count += 1
                elif 30 > float(group) > 15 :
                    count += 2
                elif float(group) > 30 :
                    count += 5
                    
        return count

    payement_missed = is_valid_grouped_string(payment_history)
    payment_history_score = 25 - payement_missed
    scorecard['Repayment History'] = payment_history_score

    from enquiries import extract_enquiry_data
    enquiries_dict = extract_enquiry_data(data)
    df_enq = pd.DataFrame(enquiries_dict)
    enquiries = df_enq["Purpose"].to_list()

    def calculate_enquiry_score(enquiries, weightage=10):
        unsecured_types = ['PERSONAL LOAN', 'CREDIT CARD', 'EDUCATIONAL LOAN']
        unsecured_count = sum(1 for e in enquiries if e in unsecured_types)

        if unsecured_count <= 2:
            deduction = 0
        elif unsecured_count <= 4:
            deduction = 2
        elif unsecured_count <= 6:
            deduction = 4
        elif unsecured_count <= 8:
            deduction = 6
        else:
            deduction = 8  # or even 10 if you want stricter rules

        return weightage - deduction

    enquiry_frequency = calculate_enquiry_score(enquiries, weightage=10)
    scorecard['Enquiry Frequency'] = enquiry_frequency


    def calculate_credit_mix_score_by_count(loan_types):
        secured_types = ['HOUSING LOAN', 'AUTO LOAN', 'GOLD LOAN']
        unsecured_types = ['PERSONAL LOAN', 'CREDIT CARD', 'EDUCATIONAL LOAN']

        secured_count = sum(1 for e in loan_types if e.upper() in secured_types)
        unsecured_count = sum(1 for e in loan_types if e.upper() in unsecured_types)
        total = secured_count + unsecured_count

        if total == 0:
            return 0.0, "No Data"

        secured_ratio = secured_count / total

        if unsecured_count == 0:
            return 10.0, "Fully Secured"
        elif secured_count == 0:
            return 5.0, "Fully Unsecured"
        elif secured_ratio >= 0.75:
            return 10.0, "Highly Secured"
        elif secured_ratio >= 0.60:
            return 9.0, "Mostly Secured"
        elif secured_ratio >= 0.50:
            return 8.0, "Balanced"
        elif secured_ratio >= 0.35:
            return 7.0, "Slightly Unsecured"
        elif secured_ratio >= 0.20:
            return 6.0, "Mostly Unsecured"
        else:
            return 5.0, "Highly Unsecured"

    loan_types = df_loan["Loan Type"].to_list()
    credit_mix_score = calculate_credit_mix_score_by_count(loan_types)
    scorecard['Credit Mix'] = credit_mix_score[0]


    secured_types = ['HOUSING LOAN', 'AUTO LOAN', 'GOLD LOAN']
    for loan in loan_types:
        if loan.upper() in secured_types:
            has_secured_loans = 10
            break
        else:
            has_secured_loans = 5

    scorecard['Has Secured Loan'] = has_secured_loans
    # print(scorecard)
    return scorecard
    

# a = loan_appraisal_scorecard(data)
# print(a)