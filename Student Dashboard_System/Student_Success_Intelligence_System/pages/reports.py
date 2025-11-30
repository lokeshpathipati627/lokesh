import streamlit as st
import pandas as pd
from pages.advisor_dashboard import load_data, synthesize_student_profile, compute_weighted_risk


def _brief_summary(row: pd.Series) -> str:
    parts = []
    gpa = row.get('gpa', None)
    if pd.notna(gpa):
        try:
            g = float(gpa)
            if g < 2.0:
                parts.append('Low GPA')
            elif g < 2.5:
                parts.append('At-risk GPA')
        except Exception:
            pass
    if float(row.get('unpaid_fees', 0) or 0) > 500:
        parts.append('Unpaid fees')
    if int(row.get('attendance_pct', 100) or 100) < 80:
        parts.append('Low attendance')
    if int(row.get('warnings_count', 0) or 0) >= 2:
        parts.append('Multiple warnings')
    if int(row.get('counseling_visits', 0) or 0) < 1 or int(row.get('engagement_score', 100) or 100) < 50:
        parts.append('Low engagement')
    if not parts:
        parts.append('No major risks')
    return ', '.join(parts[:3])


def render(navigate_to):
    st.markdown("""
    <div class="header-container">
        <div class="header-title">📑 Reports</div>
        <div class="header-subtitle">Brief risk summaries per student</div>
    </div>
    """, unsafe_allow_html=True)

    # Back to Home
    if st.button("⬅️ Back to Home", use_container_width=True):
        navigate_to('institutional')

    df = load_data()

    # Synthesize minimal attributes and risk
    out_rows = []
    for _, r in df.iterrows():
        prof = synthesize_student_profile(r)
        score, label = compute_weighted_risk(prof, r.get('gpa', None))
        brief = _brief_summary({**r.to_dict(), **prof})
        out_rows.append({
            'Student ID': r.get('student_id', ''),
            # 'Name': r.get('name', ''),
            'Risk': label,
            'Summary': f"{label} risk — {brief}"
        })

    rep = pd.DataFrame(out_rows)

    st.markdown("### Summary")
    st.dataframe(rep, use_container_width=True, hide_index=True)

    csv = rep.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, file_name="risk_report.csv", mime="text/csv")
