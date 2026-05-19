import sys
import os
import sqlite3
import random
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStackedWidget, QTableWidget,
                             QTableWidgetItem, QHeaderView, QFrame, QMessageBox, QComboBox,
                             QTextEdit, QGridLayout, QDialog, QFormLayout, QProgressBar,
                             QTabWidget, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

# --- DATABASE & CONSTANTS ---
DB_DIR = "data"
OUT_DIR = "output"
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

USER_DB = os.path.join(DB_DIR, "users.db")
MED_DB = os.path.join(OUT_DIR, "medicine.txt")
PATIENT_DB = os.path.join(DB_DIR, "patients_db.txt")
BEDS_DB = os.path.join(DB_DIR, "beds_db.txt")
DEPTS_DB = os.path.join(DB_DIR, "departments_db.txt")

def init_user_db():
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT UNIQUE,
                       password TEXT,
                       role TEXT)''')
                       
    default_users = [
        ('admin', 'admin123', 'Admin'),
        ('rec', 'rec123', 'Receptionist (A)'),
        ('doc', 'doc123', 'Doctor (B)'),
        ('pharm', 'pharm123', 'Pharmacist (C)'),
        ('ward', 'ward123', 'Ward Manager (D)')
    ]
    
    for u, p, r in default_users:
        cursor.execute("SELECT * FROM users WHERE username=?", (u,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (u, p, r))
            
    conn.commit()
    conn.close()

init_user_db()

def read_txt(filename, sep='|'):
    if not os.path.exists(filename): return []
    with open(filename, 'r', encoding='utf-8') as f:
        if sep: return [line.strip().split(sep) for line in f if line.strip()]
        else: return [line.strip().split() for line in f if line.strip()]

def write_txt(filename, data_list, sep='|'):
    with open(filename, 'w', encoding='utf-8') as f:
        for row in data_list:
            if sep: f.write(sep.join(map(str, row)) + '\n')
            else: f.write(' '.join(map(str, row)) + '\n')

# --- STYLESHEET ---
STYLE_SHEET = """
QMainWindow, QDialog { background-color: #1e1e2e; }
QLabel { color: #cdd6f4; font-size: 14px; font-family: 'Arial', sans-serif; }
QLabel#Title { font-size: 26px; font-weight: bold; color: #89b4fa; margin-bottom: 15px; }
QLabel#Header { font-size: 20px; font-weight: bold; color: #b4befe; margin-bottom: 10px; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; border-radius: 6px; padding: 6px; font-size: 13px; }
QTextEdit { background-color: #11111b; color: #a6e3a1; border: 1px solid #45475a; border-radius: 6px; padding: 10px; font-family: Consolas, monospace; }
QPushButton { background-color: #89b4fa; color: #11111b; border: none; border-radius: 6px; padding: 8px 14px; font-weight: bold; font-size: 13px; }
QPushButton:hover { background-color: #74c7ec; }
QPushButton#Secondary { background-color: #45475a; color: #cdd6f4; }
QPushButton#Secondary:hover { background-color: #585b70; }
QPushButton#Danger { background-color: #f38ba8; color: #11111b; }
QPushButton#Danger:hover { background-color: #eba0ac; }
QPushButton#Success { background-color: #a6e3a1; color: #11111b; }
QTableWidget { background-color: #181825; color: #cdd6f4; gridline-color: #313244; border: 1px solid #313244; border-radius: 6px; font-size: 13px; }
QHeaderView::section { background-color: #313244; color: #cdd6f4; padding: 6px; border: none; font-weight: bold; }
QTableWidget::item:selected { background-color: #89b4fa; color: #11111b; }
QFrame#Sidebar { background-color: #11111b; border-right: 1px solid #313244; }
QPushButton#NavBtn { background-color: transparent; color: #a6adc8; text-align: left; padding: 12px 20px; font-size: 14px; border-radius: 0px; }
QPushButton#NavBtn:hover { background-color: #313244; color: #cdd6f4; }
QPushButton#NavBtn:checked { background-color: #89b4fa; color: #11111b; font-weight: bold; border-left: 4px solid #f38ba8; }
QFrame#Card { background-color: #181825; border-radius: 8px; padding: 15px; }
QLabel#CardValue { font-size: 32px; font-weight: bold; color: #f9e2af; }
QTabWidget::pane { border: 1px solid #45475a; border-radius: 6px; background-color: #1e1e2e; }
QTabBar::tab { background-color: #181825; color: #a6adc8; padding: 8px 20px; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
QTabBar::tab:selected { background-color: #313244; color: #89b4fa; font-weight: bold; }
"""

# --- AUTHENTICATION ---
class AuthWidget(QWidget):
    login_success = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        self.is_login = True
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card.setFixedWidth(380)
        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(15)

        self.title_lbl = QLabel("Hospital Login")
        self.title_lbl.setObjectName("Title")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title_lbl)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        card_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.pass_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Receptionist (A)", "Doctor (B)", "Pharmacist (C)", "Ward Manager (D)", "Admin"])
        self.role_combo.hide()
        card_layout.addWidget(self.role_combo)

        self.action_btn = QPushButton("Login")
        self.action_btn.clicked.connect(self.handle_action)
        card_layout.addWidget(self.action_btn)

        self.toggle_btn = QPushButton("Switch to Register")
        self.toggle_btn.setObjectName("Secondary")
        self.toggle_btn.clicked.connect(self.toggle_mode)
        card_layout.addWidget(self.toggle_btn)

        layout.addWidget(self.card)

    def toggle_mode(self):
        self.is_login = not self.is_login
        self.title_lbl.setText("Hospital Login" if self.is_login else "Create Account")
        self.action_btn.setText("Login" if self.is_login else "Register")
        self.toggle_btn.setText("Switch to Register" if self.is_login else "Switch to Login")
        self.role_combo.setVisible(not self.is_login)

    def handle_action(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Fields cannot be empty!")
            return

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()
        if self.is_login:
            cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
            res = cursor.fetchone()
            if res:
                self.login_success.emit(username, res[0])
                self.user_input.clear()
                self.pass_input.clear()
            else:
                QMessageBox.critical(self, "Error", "Invalid username or password!")
        else:
            role = self.role_combo.currentText()
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
                conn.commit()
                QMessageBox.information(self, "Success", "Registration successful! You can now login.")
                self.toggle_mode()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "Username already exists!")
        conn.close()

# --- MODULE A: Outpatient & Registration ---
class OutpatientWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel("Module A: Outpatient Registration")
        lbl.setObjectName("Header")
        layout.addWidget(lbl)

        form_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Patient Name")
        
        self.dept_combo = QComboBox()
        depts = read_txt(DEPTS_DB)
        for d in depts:
            if len(d) >= 2: self.dept_combo.addItem(d[1], d[0])
            
        self.reg_btn = QPushButton("Register Patient & Assign to Queue")
        self.reg_btn.setObjectName("Success")
        self.reg_btn.clicked.connect(self.register_patient)
        
        if self.role not in ["Admin", "Receptionist (A)"]:
            self.reg_btn.setEnabled(False)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.dept_combo)
        form_layout.addWidget(self.reg_btn)
        
        layout.addLayout(form_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Patient ID", "Name", "Target Dept ID", "Ward (N/A)", "Bed (N/A)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.load_data()

    def load_data(self):
        data = read_txt(PATIENT_DB)
        outpatients = [r for r in data if len(r) >= 4 and (r[3] == '-1' or r[3] == '-2')]
        self.table.setRowCount(len(outpatients))
        for r, row_data in enumerate(outpatients):
            for c in range(min(5, len(row_data))):
                self.table.setItem(r, c, QTableWidgetItem(row_data[c]))

    def register_patient(self):
        name = self.name_input.text().strip()
        if not name: return
        dept_id = self.dept_combo.currentData()
        
        patients = read_txt(PATIENT_DB)
        new_id = str(len(patients) + 1)
        new_patient = [new_id, name, dept_id, "-1", "-1"]
        patients.append(new_patient)
        write_txt(PATIENT_DB, patients)
        
        self.name_input.clear()
        self.load_data()
        QMessageBox.information(self, "Success", f"Patient {name} registered for queue.")

# --- MODULE B: Doctor Consultation ---
class DoctorWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel("Module B: Doctor Consultation Queue")
        lbl.setObjectName("Header")
        layout.addWidget(lbl)

        ctrl_layout = QHBoxLayout()
        self.call_btn = QPushButton("Call Next Patient")
        self.call_btn.setObjectName("Success")
        self.call_btn.clicked.connect(self.call_patient)
        
        self.finish_btn = QPushButton("Finish Consultation & Prescribe")
        self.finish_btn.clicked.connect(self.finish_consultation)
        
        if self.role not in ["Admin", "Doctor (B)"]:
            self.call_btn.setEnabled(False)
            self.finish_btn.setEnabled(False)

        ctrl_layout.addWidget(self.call_btn)
        ctrl_layout.addWidget(self.finish_btn)
        ctrl_layout.addStretch()
        layout.addLayout(ctrl_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Queue ID", "Patient Name", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.load_data()

    def load_data(self):
        data = read_txt(PATIENT_DB)
        waiting = [r for r in data if len(r) >= 4 and r[3] == '-1']
        self.table.setRowCount(len(waiting))
        for r, row in enumerate(waiting):
            self.table.setItem(r, 0, QTableWidgetItem(row[0]))
            self.table.setItem(r, 1, QTableWidgetItem(row[1]))
            self.table.setItem(r, 2, QTableWidgetItem("Waiting"))

    def call_patient(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.setItem(row, 2, QTableWidgetItem("Consulting..."))
            QMessageBox.information(self, "Queue", f"Calling Patient: {self.table.item(row, 1).text()}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient to call.")

    def finish_consultation(self):
        row = self.table.currentRow()
        if row >= 0:
            p_id = self.table.item(row, 0).text()
            p_name = self.table.item(row, 1).text()
            
            patients = read_txt(PATIENT_DB)
            for p in patients:
                if p[0] == p_id:
                    p[3] = '-2'  # Mark as Consultation Finished
                    break
            write_txt(PATIENT_DB, patients)
            
            QMessageBox.information(self, "Consultation", f"Consultation finished for {p_name}. They can now go to Pharmacy or Inpatient admission.")
            self.load_data()
        else:
            QMessageBox.warning(self, "Warning", "Please select a patient to finish consultation.")

# --- MODULE C: Pharmacy ---
class PharmacyWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel("Module C: Pharmacy & Prescriptions")
        lbl.setObjectName("Header")
        layout.addWidget(lbl)

        add_layout = QHBoxLayout()
        self.m_name = QLineEdit()
        self.m_name.setPlaceholderText("Medicine Name")
        self.m_price = QSpinBox()
        self.m_price.setRange(1, 10000)
        self.m_price.setPrefix("¥ ")
        self.m_stock = QSpinBox()
        self.m_stock.setRange(0, 10000)
        
        self.add_btn = QPushButton("Add/Update Stock")
        self.add_btn.setObjectName("Success")
        self.add_btn.clicked.connect(self.add_medicine)
        
        self.dispense_btn = QPushButton("Dispense Selected")
        self.dispense_btn.setObjectName("Danger")
        self.dispense_btn.clicked.connect(self.dispense_medicine)

        if self.role not in ["Admin", "Pharmacist (C)"]:
            self.add_btn.setEnabled(False)
            self.dispense_btn.setEnabled(False)

        add_layout.addWidget(self.m_name)
        add_layout.addWidget(self.m_price)
        add_layout.addWidget(self.m_stock)
        add_layout.addWidget(self.add_btn)
        add_layout.addWidget(self.dispense_btn)
        
        layout.addLayout(add_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Price", "Stock", "Warning Line"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.load_data()

    def load_data(self):
        data = read_txt(MED_DB, sep=None)
        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c in range(min(4, len(row))):
                self.table.setItem(r, c, QTableWidgetItem(row[c]))

    def add_medicine(self):
        name = self.m_name.text().strip()
        if not name: return
        data = read_txt(MED_DB, sep=None)
        found = False
        for row in data:
            if row[0] == name:
                row[2] = str(int(row[2]) + self.m_stock.value())
                row[1] = str(self.m_price.value())
                found = True
                break
        if not found:
            data.append([name, str(self.m_price.value()), str(self.m_stock.value()), "10"])
        write_txt(MED_DB, data, sep=None)
        self.load_data()

    def dispense_medicine(self):
        row = self.table.currentRow()
        if row >= 0:
            name = self.table.item(row, 0).text()
            data = read_txt(MED_DB, sep=None)
            for r in data:
                if r[0] == name:
                    stock = int(r[2])
                    if stock > 0: r[2] = str(stock - 1)
                    else: QMessageBox.warning(self, "Out of Stock", f"{name} is out of stock!")
                    break
            write_txt(MED_DB, data, sep=None)
            self.load_data()
        else:
            QMessageBox.warning(self, "Warning", "Please select a medicine to dispense.")

# --- MODULE D: Inpatient ---
class InpatientWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel("Module D: Inpatient & Bed Management")
        lbl.setObjectName("Header")
        layout.addWidget(lbl)

        ctrl = QHBoxLayout()
        
        self.patient_combo = QComboBox()
        self.patient_combo.setMinimumWidth(200)
        ctrl.addWidget(self.patient_combo)
        
        self.assign_btn = QPushButton("Assign to Empty Bed")
        self.assign_btn.setObjectName("Success")
        self.assign_btn.clicked.connect(self.assign_bed)
        
        self.discharge_btn = QPushButton("Discharge Selected Patient")
        self.discharge_btn.setObjectName("Danger")
        self.discharge_btn.clicked.connect(self.discharge)

        if self.role not in ["Admin", "Ward Manager (D)", "Doctor (B)"]:
            self.assign_btn.setEnabled(False)
            self.discharge_btn.setEnabled(False)

        ctrl.addWidget(self.assign_btn)
        ctrl.addWidget(self.discharge_btn)
        ctrl.addStretch()
        layout.addLayout(ctrl)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Dept ID", "Ward ID", "Bed ID", "Status (1=Occ)", "Patient ID", "Patient Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.load_data()

    def load_data(self):
        data = read_txt(BEDS_DB)
        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c in range(min(6, len(row))):
                self.table.setItem(r, c, QTableWidgetItem(row[c]))
                
        self.patient_combo.clear()
        patients = read_txt(PATIENT_DB)
        unassigned = [p for p in patients if len(p) >= 4 and p[3] in ['-1', '-2']]
        for p in unassigned:
            self.patient_combo.addItem(f"{p[1]} (ID: {p[0]})", p)

    def assign_bed(self):
        p = self.patient_combo.currentData()
        if not p:
            QMessageBox.information(self, "Info", "No patients waiting for admission.")
            return

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Select an empty bed first!")
            return
            
        status = self.table.item(row, 3).text()
        if status == '1':
            QMessageBox.warning(self, "Warning", "Selected bed is already occupied!")
            return

        dept, ward, bed = self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text()
        
        beds = read_txt(BEDS_DB)
        for b in beds:
            if b[0]==dept and b[1]==ward and b[2]==bed:
                b[3] = '1'
                b[4] = p[0]
                if len(b) > 5: b[5] = p[1]
                else: b.append(p[1])
        write_txt(BEDS_DB, beds)

        patients = read_txt(PATIENT_DB)
        for pat in patients:
            if pat[0] == p[0]:
                pat[2], pat[3], pat[4] = dept, ward, bed
        write_txt(PATIENT_DB, patients)

        QMessageBox.information(self, "Success", f"Assigned {p[1]} to Ward {ward} Bed {bed}")
        self.load_data()

    def discharge(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a bed to discharge.")
            return
        status = self.table.item(row, 3).text()
        if status == '0':
            QMessageBox.warning(self, "Warning", "Selected bed is already empty!")
            return
        
        dept, ward, bed = self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text()
        pid = self.table.item(row, 4).text()

        beds = read_txt(BEDS_DB)
        for b in beds:
            if b[0]==dept and b[1]==ward and b[2]==bed:
                b[3] = '0'
                b[4] = '-1'
                if len(b) > 5: b[5] = ''
        write_txt(BEDS_DB, beds)

        patients = read_txt(PATIENT_DB)
        for p in patients:
            if p[0] == pid:
                p[3], p[4] = '-1', '-1'
        write_txt(PATIENT_DB, patients)
        
        QMessageBox.information(self, "Success", "Patient discharged.")
        self.load_data()

# --- MODULE E: Home & Report Dashboard ---
class HomeWidget(QWidget):
    def __init__(self, username, role):
        super().__init__()
        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        lbl = QLabel(f"Welcome to System Dashboard, {username} ({role})")
        lbl.setObjectName("Header")
        header_layout.addWidget(lbl)
        
        self.report_btn = QPushButton("Generate Hospital Report (D.c Equivalent)")
        self.report_btn.setObjectName("Secondary")
        self.report_btn.clicked.connect(self.generate_report)
        header_layout.addStretch()
        header_layout.addWidget(self.report_btn)
        
        layout.addLayout(header_layout)

        grid = QGridLayout()
        grid.addWidget(self.create_card("Total Outpatients", len([p for p in read_txt(PATIENT_DB) if p[3]=='-1'])), 0, 0)
        grid.addWidget(self.create_card("Total Inpatients", len([p for p in read_txt(PATIENT_DB) if p[3]!='-1'])), 0, 1)
        grid.addWidget(self.create_card("Medicine Varieties", len(read_txt(MED_DB, sep=None))), 1, 0)
        
        beds = read_txt(BEDS_DB)
        occ = sum(1 for b in beds if len(b) > 3 and b[3] == '1')
        grid.addWidget(self.create_card("Occupied Beds", occ), 1, 1)

        layout.addLayout(grid)
        layout.addStretch()

    def create_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("Card")
        l = QVBoxLayout(frame)
        t = QLabel(title)
        v = QLabel(str(value))
        v.setObjectName("CardValue")
        v.setAlignment(Qt.AlignCenter)
        l.addWidget(t)
        l.addWidget(v)
        return frame

    def generate_report(self):
        patients = read_txt(PATIENT_DB)
        beds = read_txt(BEDS_DB)
        depts = read_txt(DEPTS_DB)
        
        occ = sum(1 for b in beds if len(b) > 3 and b[3] == '1')
        t_beds = len(beds)
        t_pats = len(patients)
        t_depts = len(depts)
        
        report = f"===============================================\n"
        report += f"   HOSPITAL STATISTICS REPORT (BASED ON D.C)\n"
        report += f"===============================================\n"
        report += f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"[Hospital Overview]\n"
        report += f"Total Departments: {t_depts}\n"
        report += f"Total Patients:    {t_pats}\n"
        report += f"Total Beds:        {t_beds}\n"
        report += f"Occupied Beds:     {occ}\n"
        if t_beds > 0:
            report += f"Overall Occupancy Rate: {(occ/t_beds)*100:.1f}%\n"
        
        path = os.path.join(OUT_DIR, "hospital_report.txt")
        with open(path, "w", encoding='utf-8') as f:
            f.write(report)
        QMessageBox.information(self, "Success", f"Hospital Report exported to {path}")

# --- MODULE F: User Management (Admin Only) ---
class UserManagementWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel("Admin Only: System Users Management")
        lbl.setObjectName("Header")
        layout.addWidget(lbl)

        ctrl = QHBoxLayout()
        self.delete_btn = QPushButton("Delete Selected User")
        self.delete_btn.setObjectName("Danger")
        self.delete_btn.clicked.connect(self.delete_user)
        
        info = QLabel("Double-click any cell to edit User. Deletions are immediate.")
        info.setStyleSheet("color: #a6adc8; font-style: italic;")
        ctrl.addWidget(info)
        ctrl.addStretch()
        ctrl.addWidget(self.delete_btn)
        
        layout.addLayout(ctrl)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Password", "Role"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemChanged.connect(self.save_user)
        layout.addWidget(self.table)
        
        self.load_data()

    def load_data(self):
        self.table.blockSignals(True)
        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        
        self.table.setRowCount(len(users))
        for r, row in enumerate(users):
            item0 = QTableWidgetItem(str(row[0]))
            item0.setFlags(item0.flags() & ~Qt.ItemIsEditable) # ID cannot be edited
            self.table.setItem(r, 0, item0)
            self.table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(r, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(r, 3, QTableWidgetItem(str(row[3])))
        self.table.blockSignals(False)

    def save_user(self, item):
        row = item.row()
        uid = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        password = self.table.item(row, 2).text()
        role = self.table.item(row, 3).text()
        
        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", (username, password, role, uid))
        conn.commit()
        conn.close()

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")
            return
            
        uid = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        if username == "admin":
            QMessageBox.critical(self, "Error", "Cannot delete the master admin account!")
            return
            
        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (uid,))
        conn.commit()
        conn.close()
        self.load_data()

# --- MAIN APP ---
class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Management System - Full Program GUI")
        self.resize(1200, 750)
        self.setStyleSheet(STYLE_SHEET)

        self.central = QStackedWidget()
        self.setCentralWidget(self.central)

        self.auth = AuthWidget()
        self.auth.login_success.connect(self.setup_main_ui)
        self.central.addWidget(self.auth)

    def setup_main_ui(self, username, role):
        self.main_container = QWidget()
        layout = QHBoxLayout(self.main_container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        sb_layout = QVBoxLayout(self.sidebar)
        
        logo_lbl = QLabel("🏥 MedSystem")
        logo_lbl.setObjectName("Title")
        logo_lbl.setAlignment(Qt.AlignCenter)
        sb_layout.addWidget(logo_lbl)
        
        role_lbl = QLabel(f"Role: {role}")
        role_lbl.setAlignment(Qt.AlignCenter)
        sb_layout.addWidget(role_lbl)
        
        sb_layout.addSpacing(20)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(HomeWidget(username, role), "Dashboard & Reports")
        
        if role in ["Admin", "Receptionist (A)"]:
            self.tabs.addTab(OutpatientWidget(role), "Module A (Outpatient)")
            
        if role in ["Admin", "Doctor (B)"]:
            self.tabs.addTab(DoctorWidget(role), "Module B (Doctor)")
            
        if role in ["Admin", "Pharmacist (C)"]:
            self.tabs.addTab(PharmacyWidget(role), "Module C (Pharmacy)")
            
        if role in ["Admin", "Ward Manager (D)", "Doctor (B)"]:
            self.tabs.addTab(InpatientWidget(role), "Module D (Inpatient)")
            
        if role == "Admin":
            self.tabs.addTab(UserManagementWidget(role), "User Management")
        
        sb_layout.addStretch()
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("Secondary")
        logout_btn.clicked.connect(self.logout)
        sb_layout.addWidget(logout_btn)
        
        layout.addWidget(self.sidebar)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.addWidget(self.tabs)
        layout.addWidget(content)

        self.central.addWidget(self.main_container)
        self.central.setCurrentWidget(self.main_container)

    def logout(self):
        self.central.removeWidget(self.main_container)
        self.main_container.deleteLater()
        self.central.setCurrentWidget(self.auth)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())
