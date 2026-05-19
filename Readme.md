# 🏥 MedSystem Pro
**Advanced Enterprise Medical & Hospital Management System**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge&logo=qt)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

**MedSystem Pro** is a high-performance, lightweight desktop application designed for modern healthcare facilities. Built with Python and PyQt5, it features a sleek SaaS-inspired user interface, strict Multi-Tier Role-Based Access Control (RBAC), and a zero-configuration flat-file database system for ultimate portability and rapid deployment.

---

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [🖥️ User Interface](#️-user-interface)
- [🏗️ System Architecture](#️-system-architecture)
- [🚀 Installation & Setup](#-installation--setup)
- [🔐 Access Control & Credentials](#-access-control--credentials)
- [📦 Module Breakdown](#-module-breakdown)
- [📂 Directory Structure](#-directory-structure)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📄 License](#-license)

---

## ✨ Key Features

*   **Role-Based Access Control (RBAC):** UI dynamically adapts to the user's role (Admin, Receptionist, Doctor, Pharmacist, Ward Manager). Staff only see the modules they are authorized to use.
*   **Enterprise SaaS UI:** Clean, high-contrast workspace with a dark sidebar navigation, subtle depth shadows, and zebra-striped data grids optimized for reading dense patient data.
*   **Zero-Config Database:** No SQL server required. Uses a structured `.txt` flat-file architecture, making the application 100% portable.
*   **Executive Dashboard:** Real-time metrics tracking outpatients, admissions, pharmaceutical inventory, and facility occupancy, complete with a 1-click analytics export.
*   **End-to-End Patient Flow:** Seamlessly tracks the patient journey: `Registration` ➡️ `Consultation` ➡️ `Pharmacy` ➡️ `Ward Admission/Discharge`.

---

## 🖥️ User Interface

*(Note: Replace these placeholder paths with actual screenshots of your application in the `docs/` folder)*

| Executive Dashboard | Clinical Consultation |
|:---:|:---:|
| `<img src="docs/dashboard.png" width="400" alt="Dashboard View">` | `<img src="docs/consultation.png" width="400" alt="Doctor Module">` |
| **Pharmacy Inventory** | **Access Control (Admin)** |
| `<img src="docs/pharmacy.png" width="400" alt="Pharmacy View">` | `<img src="docs/admin.png" width="400" alt="Admin Module">` |

---

## 🏗️ System Architecture

MedSystem Pro uses a highly portable, text-based flat-file architecture separated by delimiters (`|`). The system is self-initializing—it automatically generates the required file structures and directories on its first run.

*   **Core Engine:** Python 3
*   **GUI Framework:** PyQt5 (`QStackedWidget`, `QGraphicsDropShadowEffect`, `QTableWidget`)
*   **Data Storage:** Standard UTF-8 encoded text files
*   **DPI Scaling:** Auto-enabled for 4K and Retina displays

---

## 🚀 Installation & Setup

### Prerequisites
*   [Python 3.8+](https://www.python.org/downloads/) installed on your system.
*   `pip` (Python package manager).

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/MedSystemPro.git](https://github.com/yourusername/MedSystemPro.git)
cd MedSystemPro

All Deserve By Dong Xiao Xuan and her Team 


