import streamlit as st
import sys

# Verify running through streamlit
if "streamlit.runtime.scriptrunner" not in sys.modules:
    st.error("❌ Please run with: streamlit run app.py")
    st.stop()

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="Student Success Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS Theme (Navy Blue #002855 + Gold #F5B700)
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --navy: #002855;
        --gold: #F5B700;
        --light-gray: #F8F9FA;
        --border-gray: #E9ECEF;
    }

    /* Page background */
    .main {
        background-color: #FFFFFF;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #002855 0%, #1a4d7f 100%);
        padding: 20px 30px;
        margin: -60px -30px 30px -30px;
        border-radius: 0;
    }

    .header-title {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .header-subtitle {
        color: #F5B700;
        font-size: 12px;
        margin: 5px 0 0 0;
        opacity: 0.9;
    }

    /* Navigation buttons */
    .nav-button {
        background-color: #002855;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        margin-right: 10px;
    }

    .nav-button:hover {
        background-color: #F5B700;
        color: #002855;
    }

    .nav-button.active {
        background-color: #F5B700;
        color: #002855;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .kpi-card.navy {
        border-color: #002855;
    }

    .kpi-card.gold {
        border-color: #F5B700;
    }

    .kpi-card.red {
        border-color: #EF4444;
    }

    .kpi-card.orange {
        border-color: #F97316;
    }

    .kpi-label {
        font-size: 12px;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #002855;
        margin: 8px 0;
    }

    .kpi-subtext {
        font-size: 12px;
        color: #9CA3AF;
    }

    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .risk-badge.high {
        background-color: #FEE2E2;
        color: #991B1B;
    }

    .risk-badge.medium {
        background-color: #FEF3C7;
        color: #92400E;
    }

    .risk-badge.low {
        background-color: #D1FAE5;
        color: #065F46;
    }

    /* Filter section */
    .filter-section {
        background-color: #002855;
        padding: 20px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
    }

    .filter-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        color: #F5B700;
        margin-bottom: 10px;
    }

    /* Buttons */
    button {
        background-color: #002855 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }

    button:hover {
        background-color: #F5B700 !important;
        color: #002855 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent;
        color: #6B7280;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 10px 20px;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #002855;
        border-bottom-color: #F5B700;
        font-weight: 700;
    }

    /* Alert boxes */
    .alert-box {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }

    /* Student card */
    .student-card {
        background: white;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        transition: box-shadow 0.3s ease;
    }

    .student-card:hover {
        box-shadow: 0 4px 12px rgba(0, 40, 85, 0.1);
    }

    /* Chart container */
    .chart-container {
        background: white;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .chart-title {
        font-size: 14px;
        font-weight: 700;
        color: #002855;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #F5B700;
    }

    /* Metric value */
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #002855;
    }

    .metric-label {
        font-size: 12px;
        color: #6B7280;
        font-weight: 600;
    }

    /* Responsive adjustments for narrow windows */
    @media (max-width: 900px) {
        .header-container {
            padding: 12px 14px;
            margin: -30px -14px 18px -14px;
        }

        .header-title {
            font-size: 20px;
            gap: 6px;
        }

        .header-subtitle {
            font-size: 11px;
        }

        .kpi-card {
            padding: 12px;
            margin-bottom: 12px;
        }

        .kpi-value { font-size: 22px; }
        .kpi-label, .kpi-subtext { font-size: 11px; }

        .chart-container { padding: 12px; }
        .chart-title { font-size: 13px; }

        .student-card { padding: 10px; border-radius: 6px; }
        .student-card .risk-badge { font-size: 11px; padding: 3px 10px; }

        .nav-button { padding: 8px 12px; font-size: 13px; }

        .metric-value { font-size: 18px; }

        /* reduce tab padding */
        .stTabs [data-baseweb="tab-list"] button { padding: 8px 12px; }
    }
/* Utility: ensure long text wraps nicely in alerts and cards */
    .alert-box, .student-card { word-wrap: break-word; overflow-wrap: anywhere; }
    .alert-box small { display: inline-block; margin-top: 6px; opacity: 0.85; }

    /* Improve button tap areas and spacing */
    .stButton > button { min-height: 38px !important; padding: 10px 14px !important; border-radius: 8px !important; }
    .stButton { margin-top: 4px; margin-bottom: 4px; }

    /* Make wide tables scrollable on small screens */
    .stDataFrame, .stTable { overflow-x: auto; }

    /* Additional responsive refinements */
    @media (max-width: 900px) {
        .kpi-card { margin-bottom: 10px; }
        .kpi-value { font-size: 22px; }
        .metric-value { font-size: 18px; }
        .stMetric { padding: 6px 0; }
    }

    @media (max-width: 600px) {
        .header-title { font-size: 18px; }
        .header-subtitle { font-size: 10px; }
        .nav-button { padding: 6px 10px; font-size: 12px; }
        .student-card { padding: 8px; }
        .alert-box { padding: 10px; }
        .stTabs [data-baseweb="tab-list"] button { padding: 6px 8px; font-size: 12px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "institutional"

if "selected_student_id" not in st.session_state:
    st.session_state.selected_student_id = None

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "risk_filter" not in st.session_state:
    st.session_state.risk_filter = "All"

if "interventions" not in st.session_state:
    st.session_state.interventions = {}

# Authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None

# ============================================================================
# NAVIGATION FUNCTIONS
# ============================================================================
def navigate_to(screen, student_id=None):
    """Navigate to a different screen"""
    st.session_state.current_screen = screen
    if student_id:
        st.session_state.selected_student_id = student_id
    # force a rerun so the new page renders immediately
    try:
        st.rerun()
    except Exception:
        pass

# ============================================================================
# IMPORT PAGE MODULES
# ============================================================================
from pages import institutional_dashboard, advisor_dashboard, student_detail
from pages import alerts_page
from pages import _login as login, _profile as profile

# ============================================================================
# MAIN APP ROUTING
# ============================================================================
def main():
    # If not authenticated, show login first
    if not st.session_state.get('authenticated', False):
        login.render(navigate_to)
        return

    # Render appropriate page based on session state
    if st.session_state.current_screen == "institutional":
        institutional_dashboard.render(navigate_to)
    elif st.session_state.current_screen == "advisor":
        advisor_dashboard.render(navigate_to)
    elif st.session_state.current_screen == "student-detail":
        student_detail.render(st.session_state.selected_student_id, navigate_to)
    elif st.session_state.current_screen == "alerts":
        alerts_page.render(navigate_to)
    elif st.session_state.current_screen == "profile":
        profile.render(navigate_to)

if __name__ == "__main__":
    main()
