import streamlit as st
import pandas as pd
from pages import student_detail
from pages._alerts_lib import _ensure_alerts_state, get_alerts_for_student, acknowledge_alert, send_email
from utils.alert_logic import AlertSystem


def render(navigate_to):
    st.markdown("""
    <div class='header-container'>
        <div class='header-title'>🔔 Alerts</div>
        <div class='header-subtitle'>In-app alerts for students</div>
    </div>
    """, unsafe_allow_html=True)

    _ensure_alerts_state()

    notifications = st.session_state.get('notifications', {})

    if not notifications:
        st.info("No alerts at the moment")
        return

    # Flatten notifications with student info
    for student_id, notes in notifications.items():
        if not notes:
            continue
        st.markdown(f"### Student {student_id}")
        for i, n in enumerate(notes):
            # Severity inference from subject suffix created in advisor_dashboard (e.g., "GPA - CRITICAL")
            subj = n.get('subject', '')
            sev = 'warning'
            if 'CRITICAL' in subj.upper():
                sev = 'critical'
            elif 'INFO' in subj.upper():
                sev = 'info'

            color = AlertSystem.get_alert_color(sev)
            box = st.container()
            with box:
                st.markdown(f"""
                <div style="border-left: 6px solid {color}; padding: 8px 12px; background: #fafafa; border-radius: 6px;">
                    <div><strong>{subj}</strong> — <small>{n['date']}</small></div>
                    <div style="margin-top:6px;">{n['message']}</div>
                </div>
                """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button("View Student", key=f"alert_view_{student_id}_{i}"):
                    navigate_to('student-detail', student_id)
            with col2:
                if st.button("Acknowledge", key=f"alert_ack_{student_id}_{i}"):
                    ok = acknowledge_alert(student_id, i)
                    if ok:
                        st.rerun()
                    else:
                        st.error("Failed to acknowledge")
            with col3:
                if st.button("Resend Email", key=f"alert_resend_{student_id}_{i}"):
                    to_email = f"{student_id.lower()}@example.edu"
                    sent, info = send_email(to_email, subj, n['message'])
                    if sent:
                        st.success(f"Email sent to {to_email}")
                    else:
                        st.warning(f"Email not sent: {info}")
