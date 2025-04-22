import sqlite3
from datetime import datetime

def create_tables():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    # Drop the existing ambulance table if it exists
    c.execute('DROP TABLE IF EXISTS ambulance')
    
    # Appointments Table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  patient_name TEXT NOT NULL,
                  doctor_name TEXT NOT NULL,
                  date TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    # Patients Table
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  doctor TEXT NOT NULL,
                  admit_date TEXT NOT NULL,
                  disease TEXT NOT NULL,
                  room TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    # Ambulance Table (Updated with contact column)
    c.execute('''CREATE TABLE IF NOT EXISTS ambulance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  location TEXT NOT NULL,
                  disease TEXT NOT NULL,
                  contact TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()