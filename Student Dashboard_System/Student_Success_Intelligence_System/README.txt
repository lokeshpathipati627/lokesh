
STUDENT SUCCESS INTELLIGENCE SYSTEM - SETUP & RUN INSTRUCTIONS

Authors:

Lokesh Pathipati
Shashank Reddy Paryada
Harshavardhan Reddy Putluri
Shahed Afride
Saikrishna Vennam


PROJECT OVERVIEW:
A comprehensive Streamlit-based student analytics dashboard for institutional,
advisor, and student-level insights with risk tracking and intervention management.

================================================================================
PREREQUISITES
================================================================================

1. Python 3.8+ installed
   → Check: python --version

2. Git (optional, for version control)

================================================================================
INSTALLATION STEPS
================================================================================

Step 1: Navigate to Project Directory
────────────────────────────────────────
cd Student_Success_Intelligence_System


Step 2: Create Virtual Environment (Recommended)
────────────────────────────────────────────────
On Windows PowerShell:
  python -m venv venv
  .\venv\Scripts\Activate.ps1

On Windows Command Prompt:
  python -m venv venv
  venv\Scripts\activate.bat

Step 3: Install Dependencies
────────────────────────────
pip install -r requirements.txt

This installs:
  - Streamlit (1.28+) - Web framework
  - Pandas (2.0+) - Data manipulation
  - Plotly (5.14+) - Interactive charts
  - NumPy (1.24+) - Numerical computing

================================================================================
RUNNING THE APPLICATION
================================================================================

Method 1: Run Streamlit App (Recommended)
──────────────────────────────────────────

streamlit run app.py


The dashboard will open at: http://localhost:8501

Method 2: Custom Configuration
───────────────────────────────
streamlit run app.py --logger.level=debug



================================================================================
PERFORMANCE TIPS
================================================================================

1. Clear browser cache if charts don't update
   Ctrl+Shift+Delete

2. Restart app after CSV updates
   Ctrl+C in terminal, then: streamlit run app.py

3. Check data size for large datasets
   Current mock data: 8 students (instant load)

4. Use filters to reduce chart rendering time
