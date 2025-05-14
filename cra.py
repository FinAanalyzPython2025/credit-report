import json
import pandas as pd
from flask import Flask,request, jsonify
import traceback

app = Flask(__name__)

@app.route('/api/credit-report', methods=['POST'])
def credit_report():
    try:
        # Validate file in request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        # Load JSON data
        try:
            json_data = json.load(file)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file provided"}), 400

        # ------------------------ ACCOUNTS SECTION ------------------------
        try:
            accounts = json_data['data']['credit_report'][0]['accounts']
            df = pd.DataFrame(accounts)
            df['highCreditAmount'] = pd.to_numeric(df['highCreditAmount'], errors='coerce')
            df['emiAmount'] = pd.to_numeric(df.get('emiAmount', 0), errors='coerce')

            grouped = df.groupby(['accountType', 'memberShortName'])['highCreditAmount'].sum().reset_index()
            grouped1 = df.groupby(['accountType', 'memberShortName'])[['highCreditAmount', 'emiAmount']].sum().reset_index()
        except Exception as e:
            return jsonify({"error": "Error processing accounts section", "details": str(e)}), 500
        
        # ------------------------ BASIC DETAILS ---------------------------
        from basic_details import basic_details
        details = basic_details(json_data)

        # ------------------------ ENQUIRIES SECTION ------------------------
        try:
            from enquiries import extract_enquiry_data
            enq_data = extract_enquiry_data(json_data)
            
        except Exception as e:
            return jsonify({"error": "Error processing enquiries section", "details": str(e)}), 500
        
        # ------------------------ SECURED LOANS AND COLLATERAL SECTION ------------------------
        try:
            from secured_loans import secured_loans
            sec_loan_data = secured_loans(json_data)
            
        except Exception as e:
            return jsonify({"error": "Error processing enquiries section", "details": str(e)}), 500

          
        df = pd.DataFrame(sec_loan_data[0])
        df_active_loans = df[df["Status"] == "Active"]
        active_loans = df_active_loans.to_dict(orient='records')
        # print("Credit Facilities : ","\n",df_active_loans)

        df_closed_loans = df[df["Status"] == "Closed"]
        closed_loans = df_closed_loans.to_dict(orient='records')

        df_enq_data = pd.DataFrame(enq_data)
        # print("Enquiries : ","\n",df_enq_data)

        df_sec_loan_data = pd.DataFrame(sec_loan_data[1])
        # print("Secured Loan : ","\n",df_sec_loan_data)

        # ------------------------ Loan Appraisal Scorecard ------------------------

        from loan_appraisal_scorecard import loan_appraisal_dcorecard
        params = loan_appraisal_dcorecard(json_data)
        
        return str(sum(params.values()))

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)