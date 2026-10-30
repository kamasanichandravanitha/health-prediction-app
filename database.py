import sqlite3, os

DB_PATH=os.path.join(os.path.dirname(__file__), "health_records.db")

def get_conn():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=get_conn()
    conn.execute("""CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL, dob TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
        glucose REAL NOT NULL, haemoglobin REAL NOT NULL,
        cholesterol REAL NOT NULL, remarks TEXT)""")
    conn.commit()
    conn.close()

def get_all():
    conn=get_conn()
    rows=conn.execute("SELECT * FROM patients ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_existing_emails(exclude_id=None):
    conn=get_conn()
    if exclude_id:
        rows=conn.execute("SELECT email FROM patients WHERE id != ?", (exclude_id,)).fetchall()
    else:
        rows=conn.execute("SELECT email FROM patients").fetchall()
    conn.close()
    return set(r[0].lower() for r in rows)

def create(record):
    conn=get_conn()
    cur=conn.execute("INSERT INTO patients (full_name,dob,email,glucose,haemoglobin,cholesterol,remarks) VALUES (?,?,?,?,?,?,?)",
        (record['full_name'],record['dob'],record['email'],record['glucose'],record['haemoglobin'],record['cholesterol'],record['remarks']))
    conn.commit()
    lid=cur.lastrowid
    conn.close()
    return lid

def update(pid, record):
    conn=get_conn()
    conn.execute("UPDATE patients SET full_name=?,dob=?,email=?,glucose=?,haemoglobin=?,cholesterol=?,remarks=? WHERE id=?",
        (record['full_name'],record['dob'],record['email'],record['glucose'],record['haemoglobin'],record['cholesterol'],record['remarks'],pid))
    conn.commit()
    conn.close()

def delete(pid):
    conn=get_conn()
    conn.execute("DELETE FROM patients WHERE id=?",(pid,))
    conn.commit()
    conn.close()