import streamlit as st
import database, validator, ai_api
from datetime import datetime

st.set_page_config(page_title="Health Prediction App", layout="wide")
database.init_db()

st.title("Health Prediction Application")
st.markdown("Python Developer Task 2 - Gokul Infocare")

menu = st.sidebar.selectbox("Menu", ["Add Patient", "View All", "Load Test Data"])

if menu == "Add Patient":
    st.subheader("Add / Edit Patient")
    with st.form("patient_form"):
        full_name = st.text_input("Full Name *")
        dob = st.text_input("DOB (dd.mm.yyyy) *", placeholder="28.01.1960")
        email = st.text_input("Email *", placeholder="robyn@gmail.com")
        col1, col2, col3 = st.columns(3)
        with col1: glucose = st.text_input("Glucose *", placeholder="97")
        with col2: haemoglobin = st.text_input("Haemoglobin *", placeholder="14")
        with col3: cholesterol = st.text_input("Cholesterol *", placeholder="164")
        submitted = st.form_submit_button("Save & Predict")

        if submitted:
            record = {
                'full_name': full_name, 'dob': dob, 'email': email,
                'glucose': glucose, 'haemoglobin': haemoglobin, 'cholesterol': cholesterol
            }
            existing = database.get_existing_emails()
            errors = validator.validate_full(record, existing)
            if errors:
                for e in errors: st.error(e)
            else:
                remarks = ai_api.get_health_prediction(record)
                record['remarks'] = remarks
                database.create(record)
                st.success(f"Saved! AI Prediction: {remarks}")

elif menu == "View All":
    st.subheader("All Patient Records")
    rows = database.get_all()
    if not rows:
        st.info("No records found. Add from Add Patient menu.")
    else:
        for r in rows:
            with st.expander(f"{r['id']}. {r['full_name']} - {r['email']} - {r['remarks']}"):
                st.write(f"DOB: {r['dob']} | Glucose: {r['glucose']} | Hb: {r['haemoglobin']} | Chol: {r['cholesterol']}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"Delete {r['id']}", key=f"del{r['id']}"):
                        database.delete(r['id'])
                        st.warning("Deleted! Refresh page.")
                        st.rerun()
                with c2:
                    st.write(f"Remarks: {r['remarks']}")

elif menu == "Load Test Data":
    st.subheader("Load 10 Test Records - To Show Error Handling")
    st.write("This will test 6 valid + 4 invalid as per task")
    if st.button("Load 10 Records Now"):
        # FIX 1: Clear old data so every click gives 6/4
        for old in database.get_all():
            database.delete(old['id'])
            
        test_data = [
            {"full_name":"Robyn Pears","dob":"28.01.1960","email":"robyn@gmail.com","glucose":"97","haemoglobin":"14","cholesterol":"164"},
            {"full_name":"John Hunter","dob":"15.06.1985","email":"hunter@gmail","glucose":"150","haemoglobin":"13","cholesterol":"200"},
            {"full_name":"Peter Larry","dob":"31.11.2001","email":"peter@gmail.com","glucose":"110","haemoglobin":"15","cholesterol":"180"},
            {"full_name":"Sarah Jones","dob":"12.12.1990","email":"sarah@gmail.com","glucose":"abc","haemoglobin":"12","cholesterol":"190"},
            {"full_name":"Mike Ross","dob":"01.01.2030","email":"mike@gmail.com","glucose":"90","haemoglobin":"14.5","cholesterol":"170"},
            {"full_name":"Emma Watson","dob":"10.10.1995","email":"emma@gmail.com","glucose":"95","haemoglobin":"13.5","cholesterol":"210"},
            {"full_name":"David Smith","dob":"05.05.1975","email":"david@gmail.com","glucose":"210","haemoglobin":"16","cholesterol":"250"},
            {"full_name":"Lisa Ray","dob":"20.03.1988","email":"lisa@gmail.com","glucose":"88","haemoglobin":"11","cholesterol":"165"},
            # FIX 2: Changed duplicate to unique email
            {"full_name":"Chris Evans","dob":"28.01.1960","email":"chris@gmail.com","glucose":"97","haemoglobin":"14","cholesterol":"164"},
            {"full_name":"Alex Paul","dob":"14.02.1992","email":"alex@gmail.com","glucose":"102","haemoglobin":"14.2","cholesterol":"195"},
        ]
        success=0; fail=0
        for rec in test_data:
            existing = database.get_existing_emails()
            errors = validator.validate_full(rec, existing)
            if errors:
                st.error(f"FAILED {rec['full_name']} ({rec['email']}): {', '.join(errors)}")
                fail+=1
            else:
                rec['remarks']=ai_api.get_health_prediction(rec)
                database.create(rec)
                st.success(f"SAVED {rec['full_name']} - {rec['remarks']}")
                success+=1
        st.info(f"Summary: {success} Saved, {fail} Errors detected - This is expected validation")