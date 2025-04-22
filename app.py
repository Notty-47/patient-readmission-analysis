from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'hospital.db'

# Function to create database tables
def create_tables():
    conn = sqlite3.connect(DATABASE)
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

# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return g.db

# Function to close the database connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Register the close_db function to be called when the app context tears down
app.teardown_appcontext(close_db)

# Home route
@app.route('/')
def index():
    db = get_db()
    c = db.cursor()
    
    # Count data for dashboard
    c.execute("SELECT COUNT(*) FROM appointments")
    appointments_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM patients")
    patients_count = c.fetchone()[0]
    
    return render_template('index.html',
                         appointments_count=appointments_count,
                         patients_count=patients_count)

# Route to handle appointment submissions
@app.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        date = request.form['date']
        
        db = get_db()
        c = db.cursor()
        c.execute('INSERT INTO appointments (patient_name, doctor_name, date) VALUES (?, ?, ?)',
                  (patient_name, doctor_name, date))
        db.commit()
        
    return redirect(url_for('index'))

# Route to handle patient submissions
@app.route('/submit_patient', methods=['POST'])
def submit_patient():
    if request.method == 'POST':
        name = request.form['name']
        doctor = request.form['doctor']
        admit_date = request.form['admit_date']
        disease = request.form['disease']
        room = request.form['room']
        
        db = get_db()
        c = db.cursor()
        c.execute('INSERT INTO patients (name, doctor, admit_date, disease, room) VALUES (?, ?, ?, ?, ?)',
                  (name, doctor, admit_date, disease, room))
        db.commit()
        
    return redirect(url_for('index'))

# Route to display appointments
@app.route('/appointments')
def appointments():
    db = get_db()
    c = db.cursor()
    appointments = c.execute("SELECT * FROM appointments ORDER BY date DESC").fetchall()
    return render_template('appointments.html', appointments=appointments)

# Route to display patients
@app.route('/patients')
def patients():
    db = get_db()
    c = db.cursor()
    patients = c.execute("SELECT * FROM patients ORDER BY admit_date DESC").fetchall()
    return render_template('patients.html', patients=patients)

# Route to display departments
@app.route('/departments')
def departments():
    return render_template('departments.html')

# Route to display doctors
@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

# Route to display ambulance service
@app.route('/ambulance')
def ambulance():
    return render_template('ambulance.html')

# Route to handle ambulance submissions
@app.route('/submit_ambulance', methods=['POST'])
def submit_ambulance():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        disease = request.form['disease']
        contact = request.form['contact']
        
        db = get_db()
        c = db.cursor()
        c.execute('INSERT INTO ambulance (name, location, disease, contact) VALUES (?, ?, ?, ?)',
                  (name, location, disease, contact))
        db.commit()
        
    return redirect(url_for('index'))

# Route to delete a patient
@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    db = get_db()
    c = db.cursor()
    try:
        c.execute('DELETE FROM patients WHERE id = ?', (id,))
        db.commit()
    except sqlite3.OperationalError as e:
        db.rollback()
        print(f"Database error: {e}")
    finally:
        db.close()
    return redirect(url_for('patients'))

# Run the application
if __name__ == "__main__":
    create_tables()  # Ensure tables are created when the app starts
    app.run(debug=True)  # Run in debug mode during development