import sys
import os
import random
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStackedWidget, QTableWidget,
                             QTableWidgetItem, QHeaderView, QFrame, QMessageBox, QComboBox,
                             QTextEdit, QGridLayout, QDialog, QFormLayout, QProgressBar,
                             QTabWidget, QSpinBox, QDoubleSpinBox, QGraphicsDropShadowEffect,
                             QButtonGroup, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon

# --- DATABASE & CONSTANTS (UNCHANGED) ---
DB_DIR = "data"
OUT_DIR = "output"
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

USER_DB = os.path.join(DB_DIR, "users.txt")
MED_DB = os.path.join(OUT_DIR, "medicine.txt")
PATIENT_DB = os.path.join(DB_DIR, "patients_db.txt")
BEDS_DB = os.path.join(DB_DIR, "beds_db.txt")
DEPTS_DB = os.path.join(DB_DIR, "departments_db.txt")
LOG_DB = os.path.join(OUT_DIR, "activity_log.txt")
LOGO_PATH = os.path.join(DB_DIR, "logo.svg")

CURRENT_USER = ""
CURRENT_ROLE = ""

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

def add_log(action):
    if not CURRENT_USER: return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = read_txt(LOG_DB)
    data.append([timestamp, CURRENT_USER, CURRENT_ROLE, action])
    write_txt(LOG_DB, data)

def init_user_db():
    if not os.path.exists(USER_DB):
        write_txt(USER_DB, [])
        
    data = read_txt(USER_DB)
    existing_users = [row[1] for row in data if len(row) >= 4]
    
    default_users = [
        ('admin', 'admin123', 'Admin'),
        ('rec', 'rec123', 'Receptionist (A)'),
        ('doc', 'doc123', 'Doctor (B)'),
        ('pharm', 'pharm123', 'Pharmacist (C)'),
        ('ward', 'ward123', 'Ward Manager (D)')
    ]
    
    needs_update = False
    for u, p, r in default_users:
        if u not in existing_users:
            new_id = str(len(data) + 1)
            data.append([new_id, u, p, r])
            needs_update = True
            
    if needs_update:
        write_txt(USER_DB, data)

def init_logo():
    """Generates a modern, minimalist medical cross SVG logo"""
    if not os.path.exists(LOGO_PATH):
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <!-- Background with rounded corners -->
            <rect width="100" height="100" rx="22" fill="#0284C7"/>
            <!-- Outer white circle -->
            <circle cx="50" cy="50" r="32" fill="none" stroke="#E0F2FE" stroke-width="4"/>
            <!-- Medical Cross -->
            <path d="M35 50 H65 M50 35 V65" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round"/>
        </svg>"""
        with open(LOGO_PATH, "w", encoding="utf-8") as f:
            f.write(svg_content)

init_user_db()
init_logo()

def apply_shadow(widget, radius=15, y_offset=2, alpha=15):
    """Subtle, professional drop shadow for enterprise UI"""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(radius)
    shadow.setColor(QColor(0, 0, 0, alpha))
    shadow.setOffset(0, y_offset)
    widget.setGraphicsEffect(shadow)

# --- PROFESSIONAL ENTERPRISE STYLESHEET ---
STYLE_SHEET = """
* { 
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; 
}
QMainWindow, QStackedWidget { 
    background-color: #F1F5F9; 
}
QLabel { 
    color: #334155; font-size: 14px; 
}
QLabel#Title { 
    font-size: 26px; font-weight: 700; color: #0F172A; margin-bottom: 2px; letter-spacing: -0.5px;
}
QLabel#Subtitle { 
    font-size: 14px; color: #64748B; margin-bottom: 10px; 
}
QLabel#Header { 
    font-size: 20px; font-weight: 600; color: #1E293B; margin-bottom: 10px; 
}
QLabel#CardTitle {
    font-size: 13px; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}
QLabel#CardValue { 
    font-size: 32px; font-weight: 700; color: #0284C7; 
}

/* Inputs */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { 
    background-color: #FFFFFF; 
    color: #1E293B; 
    border: 1px solid #CBD5E1; 
    border-radius: 6px; 
    padding: 8px 12px; 
    font-size: 14px; 
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0284C7;
    background-color: #FFFFFF;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView { background-color: #FFFFFF; color: #1E293B; selection-background-color: #F1F5F9; border: 1px solid #CBD5E1;}

/* Buttons */
QPushButton { 
    background-color: #0284C7; 
    color: white; 
    border: none; 
    border-radius: 6px; 
    padding: 9px 16px; 
    font-weight: 600; 
    font-size: 13px; 
}
QPushButton:hover { background-color: #0369A1; }
QPushButton:pressed { background-color: #075985; }

QPushButton#Secondary { background-color: #FFFFFF; color: #475569; border: 1px solid #CBD5E1; }
QPushButton#Secondary:hover { background-color: #F8FAFC; color: #0F172A; border: 1px solid #94A3B8;}

QPushButton#Danger { background-color: #DC2626; color: white; }
QPushButton#Danger:hover { background-color: #B91C1C; }

QPushButton#Success { background-color: #059669; color: white; }
QPushButton#Success:hover { background-color: #047857; }

/* Tables */
QTableWidget { 
    background-color: #FFFFFF; 
    color: #334155; 
    border: 1px solid #E2E8F0; 
    border-radius: 6px;
    font-size: 13px; 
    gridline-color: #E2E8F0;
}
QHeaderView::section { 
    background-color: #F8FAFC; 
    color: #475569; 
    padding: 10px 8px; 
    border: none; 
    border-bottom: 1px solid #E2E8F0; 
    border-right: 1px solid #E2E8F0;
    font-weight: 600; 
    text-align: left;
}
QTableWidget::item:selected { 
    background-color: #E0F2FE; 
    color: #0369A1; 
}

/* Structure Components */
QFrame#Sidebar { 
    background-color: #0F172A; 
}
QFrame#Card { 
    background-color: #FFFFFF; 
    border-radius: 8px; 
    border: 1px solid #E2E8F0;
}

/* Navigation Menu */
QPushButton#NavBtn { 
    background-color: transparent; 
    color: #94A3B8; 
    text-align: left; 
    padding: 12px 18px; 
    font-size: 14px; 
    font-weight: 500;
    border-radius: 6px; 
    margin: 2px 12px;
}
QPushButton#NavBtn:hover { 
    background-color: #1E293B; 
    color: #F8FAFC; 
}
QPushButton#NavBtn:checked { 
    background-color: #0284C7; 
    color: #FFFFFF; 
    font-weight: 600; 
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #F1F5F9;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #CBD5E1;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover { background: #94A3B8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; }
"""

def style_table(table):
    """Apply professional data grid properties"""
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setVisible(False) 
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setAlternatingRowColors(True) # Enterprise zebra striping
    table.setStyleSheet("alternate-background-color: #F8FAFC;")
    table.setShowGrid(True)

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
        self.card.setFixedWidth(400)
        apply_shadow(self.card, radius=20, y_offset=4, alpha=10)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 45, 40, 45)
        card_layout.setSpacing(20)

        # Header Area
        header_widget = QWidget()
        hl = QVBoxLayout(header_widget)
        hl.setContentsMargins(0,0,0,0)
        hl.setSpacing(4)
        
        self.title_lbl = QLabel("MedSystem Pro")
        self.title_lbl.setObjectName("Title")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        self.title_lbl.setStyleSheet("color: #0284C7;")
        
        self.sub_lbl = QLabel("Enterprise Authentication")
        self.sub_lbl.setObjectName("Subtitle")
        self.sub_lbl.setAlignment(Qt.AlignCenter)
        
        hl.addWidget(self.title_lbl)
        hl.addWidget(self.sub_lbl)
        card_layout.addWidget(header_widget)

        # Inputs
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Employee ID / Username")
        self.user_input.setFixedHeight(40)
        card_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(40)
        card_layout.addWidget(self.pass_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Receptionist (A)", "Doctor (B)", "Pharmacist (C)", "Ward Manager (D)", "Admin"])
        self.role_combo.setFixedHeight(40)
        self.role_combo.hide()
        card_layout.addWidget(self.role_combo)

        # Buttons
        self.action_btn = QPushButton("Secure Login")
        self.action_btn.setFixedHeight(42)
        self.action_btn.clicked.connect(self.handle_action)
        card_layout.addWidget(self.action_btn)
        
        card_layout.addSpacing(10)

        self.toggle_btn = QPushButton("Register New Personnel")
        self.toggle_btn.setObjectName("Secondary")
        self.toggle_btn.setFixedHeight(40)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        card_layout.addWidget(self.toggle_btn)

        layout.addWidget(self.card)

    def toggle_mode(self):
        self.is_login = not self.is_login
        self.sub_lbl.setText("Enterprise Authentication" if self.is_login else "System Personnel Registration")
        self.action_btn.setText("Secure Login" if self.is_login else "Register User")
        self.toggle_btn.setText("Register New Personnel" if self.is_login else "Return to Login")
        self.role_combo.setVisible(not self.is_login)

    def handle_action(self):
        global CURRENT_USER, CURRENT_ROLE
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Required fields cannot be empty.")
            return

        data = read_txt(USER_DB)
        if self.is_login:
            res = next((row for row in data if len(row)>=4 and row[1]==username and row[2]==password), None)
            if res:
                CURRENT_USER = username
                CURRENT_ROLE = res[3]
                add_log("Logged into system")
                self.login_success.emit(username, res[3])
                self.user_input.clear()
                self.pass_input.clear()
            else:
                QMessageBox.critical(self, "Authentication Failed", "Invalid credentials provided.")
        else:
            role = self.role_combo.currentText()
            if any(row[1] == username for row in data if len(row)>=4):
                QMessageBox.warning(self, "Validation Error", "Username already exists in the system.")
            else:
                new_id = str(len(data) + 1)
                data.append([new_id, username, password, role])
                write_txt(USER_DB, data)
                CURRENT_USER = username
                CURRENT_ROLE = role
                add_log("Registered new account")
                CURRENT_USER = ""
                CURRENT_ROLE = ""
                QMessageBox.information(self, "Registration Success", "Personnel registered successfully.")
                self.toggle_mode()

# --- MODULE A: Outpatient & Registration ---
class OutpatientWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        lbl = QLabel("Outpatient Registration")
        lbl.setObjectName("Title")
        layout.addWidget(lbl)

        # Form Card
        form_card = QFrame()
        form_card.setObjectName("Card")
        apply_shadow(form_card)
        form_layout = QHBoxLayout(form_card)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(15)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Patient Legal Name")
        
        self.dept_combo = QComboBox()
        self.dept_combo.setMinimumWidth(220)
        depts = read_txt(DEPTS_DB)
        for d in depts:
            if len(d) >= 2: self.dept_combo.addItem(d[1], d[0])
            
        self.reg_btn = QPushButton("Register to Queue")
        self.reg_btn.setObjectName("Success")
        self.reg_btn.setMinimumWidth(160)
        self.reg_btn.clicked.connect(self.register_patient)
        
        if self.role not in ["Admin", "Receptionist (A)"]:
            self.reg_btn.setEnabled(False)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.dept_combo)
        form_layout.addWidget(self.reg_btn)
        layout.addWidget(form_card)
        
        # Table Card
        table_card = QFrame()
        table_card.setObjectName("Card")
        apply_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(25, 25, 25, 25)
        
        lbl_list = QLabel("Active Outpatient Queue")
        lbl_list.setObjectName("CardTitle")
        tl.addWidget(lbl_list)
        tl.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Patient ID", "Full Name", "Target Dept ID", "Ward (N/A)", "Bed (N/A)"])
        style_table(self.table)
        tl.addWidget(self.table)
        
        layout.addWidget(table_card)
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
        
        add_log(f"Registered Outpatient: {name}")
        
        self.name_input.clear()
        self.load_data()
        QMessageBox.information(self, "System Update", f"Patient {name} has been added to the queue.")

# --- MODULE B: Doctor Consultation ---
class DoctorWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        lbl = QLabel("Clinical Consultation Board")
        lbl.setObjectName("Title")
        layout.addWidget(lbl)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("Card")
        apply_shadow(ctrl_card)
        ctrl_layout = QHBoxLayout(ctrl_card)
        ctrl_layout.setContentsMargins(25, 25, 25, 25)
        
        self.call_btn = QPushButton("Admit Next Patient")
        self.call_btn.setObjectName("Success")
        self.call_btn.clicked.connect(self.call_patient)
        
        self.finish_btn = QPushButton("Conclude & Prescribe")
        self.finish_btn.clicked.connect(self.finish_consultation)
        
        if self.role not in ["Admin", "Doctor (B)"]:
            self.call_btn.setEnabled(False)
            self.finish_btn.setEnabled(False)

        ctrl_layout.addWidget(self.call_btn)
        ctrl_layout.addWidget(self.finish_btn)
        ctrl_layout.addStretch()
        layout.addWidget(ctrl_card)
        
        table_card = QFrame()
        table_card.setObjectName("Card")
        apply_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(25, 25, 25, 25)
        
        lbl_list = QLabel("Patient Waiting List")
        lbl_list.setObjectName("CardTitle")
        tl.addWidget(lbl_list)
        tl.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Queue ID", "Patient Name", "Current Status"])
        style_table(self.table)
        tl.addWidget(self.table)
        layout.addWidget(table_card)
        
        self.load_data()

    def load_data(self):
        data = read_txt(PATIENT_DB)
        waiting = [r for r in data if len(r) >= 4 and r[3] == '-1']
        self.table.setRowCount(len(waiting))
        for r, row in enumerate(waiting):
            self.table.setItem(r, 0, QTableWidgetItem(row[0]))
            self.table.setItem(r, 1, QTableWidgetItem(row[1]))
            self.table.setItem(r, 2, QTableWidgetItem("Awaiting Doctor"))

    def call_patient(self):
        row = self.table.currentRow()
        if row >= 0:
            p_name = self.table.item(row, 1).text()
            self.table.setItem(row, 2, QTableWidgetItem("In Consultation"))
            add_log(f"Started consultation for: {p_name}")
            QMessageBox.information(self, "System Notice", f"Patient Called: {p_name}")
        else:
            QMessageBox.warning(self, "Validation Error", "Please select a patient record first.")

    def finish_consultation(self):
        row = self.table.currentRow()
        if row >= 0:
            p_id = self.table.item(row, 0).text()
            p_name = self.table.item(row, 1).text()
            
            patients = read_txt(PATIENT_DB)
            for p in patients:
                if p[0] == p_id:
                    p[3] = '-2' 
                    break
            write_txt(PATIENT_DB, patients)
            
            add_log(f"Finished consultation for: {p_name}")
            QMessageBox.information(self, "System Update", f"Consultation recorded for {p_name}.")
            self.load_data()
        else:
            QMessageBox.warning(self, "Validation Error", "Please select an active consultation to conclude.")

# --- MODULE C: Pharmacy ---
class PharmacyWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        lbl = QLabel("Pharmacy Dispensary & Inventory")
        lbl.setObjectName("Title")
        layout.addWidget(lbl)

        add_card = QFrame()
        add_card.setObjectName("Card")
        apply_shadow(add_card)
        add_layout = QHBoxLayout(add_card)
        add_layout.setContentsMargins(25, 25, 25, 25)
        add_layout.setSpacing(15)
        
        self.m_name = QLineEdit()
        self.m_name.setPlaceholderText("Pharmaceutical Name")
        
        self.m_price = QSpinBox()
        self.m_price.setRange(1, 10000)
        self.m_price.setPrefix("USD $ ")
        
        self.m_stock = QSpinBox()
        self.m_stock.setRange(0, 10000)
        self.m_stock.setPrefix("Units: ")
        
        self.add_btn = QPushButton("Update Inventory")
        self.add_btn.setObjectName("Success")
        self.add_btn.clicked.connect(self.add_medicine)
        
        self.dispense_btn = QPushButton("Dispense Unit")
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
        layout.addWidget(add_card)
        
        table_card = QFrame()
        table_card.setObjectName("Card")
        apply_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(25, 25, 25, 25)
        
        lbl_list = QLabel("Inventory Master Ledger")
        lbl_list.setObjectName("CardTitle")
        tl.addWidget(lbl_list)
        tl.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Pharmaceutical Name", "Unit Cost", "Stock Level", "Threshold Line"])
        style_table(self.table)
        tl.addWidget(self.table)
        layout.addWidget(table_card)
        
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
        
        add_log(f"Added/Updated Medicine Stock: {name} (+{self.m_stock.value()})")
        self.load_data()

    def dispense_medicine(self):
        row = self.table.currentRow()
        if row >= 0:
            name = self.table.item(row, 0).text()
            data = read_txt(MED_DB, sep=None)
            for r in data:
                if r[0] == name:
                    stock = int(r[2])
                    if stock > 0: 
                        r[2] = str(stock - 1)
                        add_log(f"Dispensed Medicine: {name}")
                    else: 
                        QMessageBox.warning(self, "Inventory Alert", f"{name} inventory is depleted.")
                    break
            write_txt(MED_DB, data, sep=None)
            self.load_data()
        else:
            QMessageBox.warning(self, "Validation Error", "Select a pharmaceutical record to dispense.")

# --- MODULE D: Inpatient ---
class InpatientWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        lbl = QLabel("Ward Allocation & Admissions")
        lbl.setObjectName("Title")
        layout.addWidget(lbl)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("Card")
        apply_shadow(ctrl_card)
        ctrl = QHBoxLayout(ctrl_card)
        ctrl.setContentsMargins(25, 25, 25, 25)
        
        self.patient_combo = QComboBox()
        self.patient_combo.setMinimumWidth(280)
        ctrl.addWidget(self.patient_combo)
        
        self.assign_btn = QPushButton("Process Admission")
        self.assign_btn.setObjectName("Success")
        self.assign_btn.clicked.connect(self.assign_bed)
        
        self.discharge_btn = QPushButton("Process Discharge")
        self.discharge_btn.setObjectName("Danger")
        self.discharge_btn.clicked.connect(self.discharge)

        if self.role not in ["Admin", "Ward Manager (D)", "Doctor (B)"]:
            self.assign_btn.setEnabled(False)
            self.discharge_btn.setEnabled(False)

        ctrl.addWidget(self.assign_btn)
        ctrl.addWidget(self.discharge_btn)
        ctrl.addStretch()
        layout.addWidget(ctrl_card)

        table_card = QFrame()
        table_card.setObjectName("Card")
        apply_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(25, 25, 25, 25)
        
        lbl_list = QLabel("Facility Bed Ledger")
        lbl_list.setObjectName("CardTitle")
        tl.addWidget(lbl_list)
        tl.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Dept ID", "Ward ID", "Bed ID", "Status (1=Occ)", "Patient ID", "Patient Name"])
        style_table(self.table)
        tl.addWidget(self.table)
        layout.addWidget(table_card)
        
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
            self.patient_combo.addItem(f"{p[1]} (Reg ID: {p[0]})", p)

    def assign_bed(self):
        p = self.patient_combo.currentData()
        if not p:
            QMessageBox.information(self, "System Notice", "No pending admissions.")
            return

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Validation Error", "Select an available facility bed.")
            return
            
        status = self.table.item(row, 3).text()
        if status == '1':
            QMessageBox.warning(self, "Validation Error", "Target bed is currently allocated.")
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

        add_log(f"Assigned bed (Ward {ward}, Bed {bed}) to Patient: {p[1]}")
        QMessageBox.information(self, "System Update", f"Admission complete: {p[1]} assigned to Ward {ward}, Bed {bed}.")
        self.load_data()

    def discharge(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Validation Error", "Select a bed to initiate discharge.")
            return
        status = self.table.item(row, 3).text()
        if status == '0':
            QMessageBox.warning(self, "Validation Error", "Selected bed is already vacant.")
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
        
        add_log(f"Discharged bed (Ward {ward}, Bed {bed})")
        QMessageBox.information(self, "System Update", "Patient discharge processed successfully.")
        self.load_data()

# --- MODULE E: Home & Report Dashboard ---
class HomeWidget(QWidget):
    def __init__(self, username, role):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        lbl = QLabel(f"Executive Dashboard")
        lbl.setObjectName("Title")
        sub = QLabel(f"Welcome back, {username}. Facility overview & real-time metrics.")
        sub.setObjectName("Subtitle")
        title_box.addWidget(lbl)
        title_box.addWidget(sub)
        header_layout.addLayout(title_box)
        
        self.report_btn = QPushButton("Export Analytics Report")
        self.report_btn.setObjectName("Secondary")
        self.report_btn.setFixedHeight(42)
        self.report_btn.clicked.connect(self.generate_report)
        header_layout.addStretch()
        header_layout.addWidget(self.report_btn)
        
        layout.addLayout(header_layout)

        grid = QGridLayout()
        grid.setSpacing(25)
        grid.addWidget(self.create_card("Total Outpatients", len([p for p in read_txt(PATIENT_DB) if p[3]=='-1'])), 0, 0)
        grid.addWidget(self.create_card("Active Admissions", len([p for p in read_txt(PATIENT_DB) if p[3]!='-1'])), 0, 1)
        grid.addWidget(self.create_card("Pharmaceutical SKU Count", len(read_txt(MED_DB, sep=None))), 1, 0)
        
        beds = read_txt(BEDS_DB)
        occ = sum(1 for b in beds if len(b) > 3 and b[3] == '1')
        grid.addWidget(self.create_card("Facility Occupancy", occ), 1, 1)

        layout.addLayout(grid)
        layout.addStretch()

    def create_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("Card")
        apply_shadow(frame)
        l = QVBoxLayout(frame)
        l.setContentsMargins(30, 35, 30, 35)
        
        t = QLabel(title)
        t.setObjectName("CardTitle")
        v = QLabel(str(value))
        v.setObjectName("CardValue")
        
        l.addWidget(t)
        l.addSpacing(5)
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
        report += f"   ENTERPRISE FACILITY REPORT\n"
        report += f"===============================================\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"[Facility Overview]\n"
        report += f"Operational Departments: {t_depts}\n"
        report += f"Total Patient Records:   {t_pats}\n"
        report += f"Total Facility Beds:     {t_beds}\n"
        report += f"Currently Allocated:     {occ}\n"
        if t_beds > 0:
            report += f"Occupancy Rate:          {(occ/t_beds)*100:.1f}%\n"
        
        path = os.path.join(OUT_DIR, "hospital_report.txt")
        with open(path, "w", encoding='utf-8') as f:
            f.write(report)
        add_log("Generated Hospital Statistics Report")
        QMessageBox.information(self, "Export Complete", f"Data exported successfully to: {path}")

# --- MODULE F: User Management (Admin Only) ---
class UserManagementWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        lbl = QLabel("Personnel Access Control")
        lbl.setObjectName("Title")
        layout.addWidget(lbl)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("Card")
        apply_shadow(ctrl_card)
        ctrl = QHBoxLayout(ctrl_card)
        ctrl.setContentsMargins(25, 25, 25, 25)
        
        self.delete_btn = QPushButton("Revoke Personnel Access")
        self.delete_btn.setObjectName("Danger")
        self.delete_btn.clicked.connect(self.delete_user)
        
        info = QLabel("Double-click records to modify. Revocations are immediate.")
        info.setStyleSheet("color: #64748B; font-size: 13px;")
        ctrl.addWidget(info)
        ctrl.addStretch()
        ctrl.addWidget(self.delete_btn)
        
        layout.addWidget(ctrl_card)

        table_card = QFrame()
        table_card.setObjectName("Card")
        apply_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(25, 25, 25, 25)
        
        lbl_list = QLabel("Active Directory Ledger")
        lbl_list.setObjectName("CardTitle")
        tl.addWidget(lbl_list)
        tl.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Emp ID", "Username", "Security Key", "Authorization Role"])
        style_table(self.table)
        self.table.setSelectionBehavior(QTableWidget.SelectItems) 
        self.table.itemChanged.connect(self.save_user)
        tl.addWidget(self.table)
        
        layout.addWidget(table_card)
        self.load_data()

    def load_data(self):
        self.table.blockSignals(True)
        users = read_txt(USER_DB)
        
        self.table.setRowCount(len(users))
        for r, row in enumerate(users):
            if len(row) < 4: continue
            item0 = QTableWidgetItem(str(row[0]))
            item0.setFlags(item0.flags() & ~Qt.ItemIsEditable) 
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
        
        users = read_txt(USER_DB)
        for u in users:
            if len(u) >= 4 and u[0] == uid:
                u[1], u[2], u[3] = username, password, role
                break
        write_txt(USER_DB, users)
        add_log(f"Updated user: {username} ({role})")

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Validation Error", "Select a personnel record to revoke.")
            return
            
        uid = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        
        if username == "admin":
            QMessageBox.critical(self, "Security Error", "Master Administrator access cannot be revoked.")
            return
            
        users = read_txt(USER_DB)
        users = [u for u in users if len(u)>=4 and u[0] != uid]
        write_txt(USER_DB, users)
        
        add_log(f"Deleted user: {username}")
        self.load_data()

# --- MODULE G: System Activity (Admin Only) ---
class SystemActivityWidget(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        lbl = QLabel("System Activity Audit")
        lbl.setObjectName("Title")
        layout.addWidget(lbl)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("Card")
        apply_shadow(ctrl_card)
        ctrl = QHBoxLayout(ctrl_card)
        ctrl.setContentsMargins(25, 25, 25, 25)
        
        info = QLabel("Immutable audit log of all system interactions.")
        info.setStyleSheet("color: #64748B; font-size: 13px;")
        
        self.refresh_btn = QPushButton("Refresh Activity Log")
        self.refresh_btn.setObjectName("Secondary")
        self.refresh_btn.clicked.connect(self.load_data)
        
        ctrl.addWidget(info)
        ctrl.addStretch()
        ctrl.addWidget(self.refresh_btn)
        layout.addWidget(ctrl_card)

        table_card = QFrame()
        table_card.setObjectName("Card")
        apply_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(25, 25, 25, 25)
        
        lbl_list = QLabel("Event History Ledger")
        lbl_list.setObjectName("CardTitle")
        tl.addWidget(lbl_list)
        tl.addSpacing(10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Personnel Username", "Authorized Role", "System Action Executed"])
        style_table(self.table)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        tl.addWidget(self.table)
        
        layout.addWidget(table_card)
        
        self.load_data()

    def load_data(self):
        data = read_txt(LOG_DB)
        self.table.setRowCount(len(data))
        for r, row in enumerate(reversed(data)): 
            for c in range(min(4, len(row))):
                self.table.setItem(r, c, QTableWidgetItem(str(row[c])))

# --- MAIN APP ---
class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MedSystem Pro - Enterprise Management")
        
        # --- NEW LOGO ADDED HERE ---
        self.setWindowIcon(QIcon(LOGO_PATH))
        
        self.resize(1350, 850)
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
        layout.setSpacing(0)
        
        # --- SIDEBAR NAV ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(280)
        sb_layout = QVBoxLayout(self.sidebar)
        sb_layout.setContentsMargins(0, 40, 0, 30)
        sb_layout.setSpacing(8)
        
        logo_lbl = QLabel("MedSystem Pro")
        logo_lbl.setAlignment(Qt.AlignCenter)
        logo_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFFFFF; margin-bottom: 2px;")
        sb_layout.addWidget(logo_lbl)
        
        role_lbl = QLabel(f"Auth Level: {role.split(' ')[0]}")
        role_lbl.setAlignment(Qt.AlignCenter)
        role_lbl.setStyleSheet("color: #94A3B8; font-size: 13px; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 0.5px;")
        sb_layout.addWidget(role_lbl)
        
        # Nav Buttons logic via QButtonGroup
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.stack = QStackedWidget()

        # Helper to add modules cleanly
        self.page_idx = 0
        def add_nav_item(title_text, module_widget):
            btn = QPushButton(title_text)
            btn.setObjectName("NavBtn")
            btn.setCheckable(True)
            self.nav_group.addButton(btn, self.page_idx)
            sb_layout.addWidget(btn)
            self.stack.addWidget(module_widget)
            if self.page_idx == 0:
                btn.setChecked(True)
            self.page_idx += 1

        # Build Navigation Dynamically
        add_nav_item("Executive Dashboard", HomeWidget(username, role))
        
        if role in ["Admin", "Receptionist (A)"]:
            add_nav_item("Outpatient Registration", OutpatientWidget(role))
            
        if role in ["Admin", "Doctor (B)"]:
            add_nav_item("Clinical Consultation", DoctorWidget(role))
            
        if role in ["Admin", "Pharmacist (C)"]:
            add_nav_item("Pharmacy Inventory", PharmacyWidget(role))
            
        if role in ["Admin", "Ward Manager (D)", "Doctor (B)"]:
            add_nav_item("Facility Admissions", InpatientWidget(role))
            
        if role == "Admin":
            add_nav_item("Access Control", UserManagementWidget(role))
            add_nav_item("Audit Activity", SystemActivityWidget(role))
            
        self.nav_group.idClicked.connect(self.stack.setCurrentIndex)
        
        sb_layout.addStretch()
        
        # Logout
        logout_container = QWidget()
        ll = QVBoxLayout(logout_container)
        ll.setContentsMargins(25, 0, 25, 0)
        logout_btn = QPushButton("End Session")
        logout_btn.setStyleSheet("background-color: #1E293B; color: #CBD5E1; border: 1px solid #334155;")
        logout_btn.clicked.connect(self.logout)
        ll.addWidget(logout_btn)
        sb_layout.addWidget(logout_container)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        self.central.addWidget(self.main_container)
        self.central.setCurrentWidget(self.main_container)

    def logout(self):
        add_log("Logged out of system")
        global CURRENT_USER, CURRENT_ROLE
        CURRENT_USER = ""
        CURRENT_ROLE = ""
        
        self.central.removeWidget(self.main_container)
        self.main_container.deleteLater()
        self.central.setCurrentWidget(self.auth)

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())