import time
from datetime import datetime

def call_external_ai_api(glucose, haemoglobin, cholesterol, age):
    time.sleep(0.3)
    remarks=[]; risk=0
    if glucose>=200: 
        remarks.append("High Glucose - Diabetes risk")
        risk+=2
    elif glucose>=140: 
        remarks.append("Pre-diabetic")
        risk+=1
    if haemoglobin<12: 
        remarks.append("Low Haemoglobin - Anemia")
        risk+=1
    elif haemoglobin>17.5: 
        remarks.append("High Haemoglobin")
        risk+=1
    if cholesterol>=240: 
        remarks.append("High Cholesterol - Cardiovascular risk")
        risk+=2
    elif cholesterol>=200: 
        remarks.append("Borderline Cholesterol")
        risk+=1
    if risk==0: 
        final="Normal - Healthy"
    elif risk==1: 
        final="Mild Concern - "+"; ".join(remarks)
    elif risk==2: 
        final="Moderate Risk - "+"; ".join(remarks)
    else: 
        final="High Risk - "+"; ".join(remarks)
    return final

def get_health_prediction(record):
    try:
        dob=datetime.strptime(record['dob'], "%d.%m.%Y")
        age=(datetime.now()-dob).days//365
    except: 
        age=35
    return call_external_ai_api(float(record['glucose']), float(record['haemoglobin']), float(record['cholesterol']), age)