import datetime as dt
import pandas as pd
import json
from flask import jsonify

def basic_details(json_data):
    try:
        name = json_data['data']['name']
        gender = json_data['data']['gender']
        credit_score = json_data['data']['credit_score']
        pan = json_data['data']['pan']
        mobile = json_data['data']['mobile']
        dob = json_data['data']['credit_report'][0]['names'][0]['birthDate']
        # print(name, gender, credit_score, pan, mobile, dob)
        # Create a DataFrame from the extracted values
        df_ac_details = {
            'name': name,
            'gender': gender,
            'credit_score': credit_score,
            'pan': pan,
            'mobile': mobile,
            'dob': dob
        }

        return df_ac_details       
    except Exception as e:
        return jsonify({"error": "Error processing basic details", "details": str(e)}), 500