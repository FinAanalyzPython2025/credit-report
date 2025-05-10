import json
import pandas as pd
import json
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

        # ------------------------ ENQUIRIES SECTION ------------------------
        try:
            enquiries = json_data['data']['credit_report'][0].get('enquiries', [])
            if enquiries:
                enquiry_df = pd.DataFrame(enquiries)
                enquiry_df['enquiryAmount'] = pd.to_numeric(enquiry_df.get('enquiryAmount', 0), errors='coerce')

                grouped_enquiry = enquiry_df.groupby(['memberShortName', 'enquiryPurpose'])['enquiryAmount'].sum().reset_index()
            else:
                enquiry_df = pd.DataFrame()
                grouped_enquiry = pd.DataFrame()
        except Exception as e:
            return jsonify({"error": "Error processing enquiries section", "details": str(e)}), 500

        # Convert DataFrames to JSON serializable format
        return jsonify({
            "grouped_high_credit": grouped.to_dict(orient='records'),
            "grouped_high_credit_emi": grouped1.to_dict(orient='records'),
            "enquiry_data": enquiry_df.to_dict(orient='records'),
            "grouped_enquiry": grouped_enquiry.to_dict(orient='records')
        }), 200

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500
