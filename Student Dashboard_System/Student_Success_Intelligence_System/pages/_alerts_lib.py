import os
import ssl
import smtplib
from email.message import EmailMessage
from datetime import datetime
import streamlit as st
from typing import List, Dict, Tuple, Optional


def _ensure_alerts_state() -> None:
    """Ensure the session_state containers for alerts and interventions exist."""
    if 'notifications' not in st.session_state:
        st.session_state['notifications'] = {}  # student_id -> list[dict]
    if 'alert_acknowledged' not in st.session_state:
        st.session_state['alert_acknowledged'] = set()
    if 'interventions' not in st.session_state:
        st.session_state['interventions'] = {}


def add_alert(student_id: str, subject: str, message: str, advisor: str = 'Advisor') -> Dict:
    """Add an in-app alert/notification for a student and return the note dict."""
    _ensure_alerts_state()
    note = {
        'subject': subject,
        'message': message,
        'advisor': advisor,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'acknowledged': False,
    }
    st.session_state['notifications'].setdefault(student_id, []).append(note)
    return note


def get_alerts_for_student(student_id: str) -> List[Dict]:
    _ensure_alerts_state()
    return st.session_state['notifications'].get(student_id, [])


def acknowledge_alert(student_id: str, index: int) -> bool:
    """Mark an alert acknowledged and optionally record an intervention entry.

    Returns True if successful, False otherwise.
    """
    _ensure_alerts_state()
    try:
        notes = st.session_state['notifications'].get(student_id, [])
        if index < 0 or index >= len(notes):
            return False
        note = notes.pop(index)
        st.session_state['alert_acknowledged'].add(student_id)

        # record a short intervention entry automatically
        intervention = {
            'type': 'Notification Acknowledged',
            'advisor': note.get('advisor', 'Advisor'),
            'notes': note.get('message', ''),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state['interventions'].setdefault(student_id, []).append(intervention)
        return True
    except Exception:
        return False


def send_email(to_address: str, subject: str, body: str) -> Tuple[bool, str]:
    """Attempt to send an email using SMTP settings from environment variables.

    If SMTP config is missing this returns (False, message) and does not raise.
    Environment variables used:
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
    """
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = os.environ.get('SMTP_PORT')
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASSWORD')
    email_from = os.environ.get('EMAIL_FROM')

    if not (smtp_host and smtp_port and smtp_user and smtp_pass and email_from):
        return False, "SMTP not configured. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM env vars to enable email sending."

    try:
        port = int(smtp_port)
    except Exception:
        return False, "Invalid SMTP_PORT"

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = to_address
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, port, context=context) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        return True, 'Email sent'
    except Exception as e:
        return False, f'Email error: {e}'
