import re
from datetime import datetime, date

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_dob(dob_str):
    try:
        dt = datetime.strptime(dob_str.strip(), "%d.%m.%Y").date()
        if dt > date.today():
            return False, "DOB cannot be future date"
        return True, dt
    except ValueError as e:
        return False, f"Invalid date: {e}"

def validate_numeric(name, value, min_val=0, max_val=1000):
    try:
        v = float(value)
        if v < min_val or v > max_val:
            return False, f"{name} out of range"
        return True, v
    except:
        return False, f"{name} must be numeric"

def validate_full(record, existing_emails=None):
    errors=[]
    if not record.get('full_name') or len(record['full_name'].strip())<2:
        errors.append("Full Name required")
    ok, msg = validate_dob(record.get('dob',''))
    if not ok: errors.append(msg)
    if not validate_email(record.get('email','')):
        errors.append(f"Invalid email: {record.get('email')}")
    if existing_emails and record.get('email','').lower() in existing_emails:
        errors.append(f"Duplicate email")
    for field, minv, maxv in [('glucose',20,600),('haemoglobin',3,25),('cholesterol',50,600)]:
        ok2, msg2 = validate_numeric(field, record.get(field), minv, maxv)
        if not ok2: errors.append(msg2)
    return errors