# Smart Study Planner & Wellness Tracker

This is a Streamlit web application designed for students to manage their academic tasks and track their personal wellness. It integrates with a MySQL database and leverages existing triggers, stored procedures, and functions to demonstrate advanced database concepts.

## 🚀 How to Run the Application

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Then, install the required packages using pip:
```powershell
pip install -r requirements.txt
```

### 2. Configure Database Credentials
The application connects to a MySQL database. Open `db_connection.py` and update the `db_config` dictionary with your MySQL server details if they are different from the default.

Important: Ensure the `studywelldb` database and all specified Triggers, Stored Procedures, and Functions have been created on your MySQL server before running the app.

### 3. Run the Streamlit App
From the project root directory run:
```powershell
streamlit run app.py
```

## ✅ DBMS Viva Demo Checklist
This checklist outlines the key database interactions to demonstrate during a presentation or viva.

- Register a new user → `sp_RegisterUserWithSemester` (Stored Procedure)
- Mark a task complete → `sp_CompleteTask` (Stored Procedure)
- Log 3 consecutive high stress days → `trg_CheckConsecutiveHighStress` (Trigger)
- Complete prerequisite task to unlock another → `trg_UnlockDependentTask` (Trigger)
- Student dashboard uses `fn_GetAverageStress` and `fn_IsTaskUnlocked` (Functions)

