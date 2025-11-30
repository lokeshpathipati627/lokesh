import streamlit as st
from pathlib import Path

# Simple in-memory credentials for demo. In production replace with secure auth.
_USERS = {
    'advisor1': 'password123',
    'admin': 'adminpass'
}

def _render_header_and_logo():
    """
    Render Horizon State University heading and a centered logo from img/logo.png.
    If the logo is missing, the UI remains clean with a subtle placeholder.
    """
    st.markdown("""
    <style>
      :root {
        --hsu-primary: #002855;
        --hsu-muted: #666666;
        --hsu-border: #e6e8eb;
        --hsu-bg: #ffffff;
      }
      .hsu-header { display:flex; flex-direction:column; align-items:center; gap:6px; margin: 4px 0 12px; }
      .hsu-header h1 { margin:0; color:var(--hsu-primary); font-family:system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-weight:700; letter-spacing:0.2px; font-size: clamp(22px, 3.3vw, 28px); }
      .hsu-subtitle { color:var(--hsu-muted); font-size:13px; }
      .login-card { background:var(--hsu-bg); border:1px solid var(--hsu-border); border-radius:12px; padding:24px; box-shadow:0 2px 10px rgba(0,0,0,0.06); }
      .login-title { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
      .login-title h2 { color:var(--hsu-primary); margin:0; font-size: clamp(18px, 3vw, 22px); }
      .login-subtitle { color:var(--hsu-muted); font-size:13px; margin-bottom:16px; }
      .login-footer { color:#8a8a8a; font-size:12px; text-align:center; margin-top:8px; }
    </style>
    """, unsafe_allow_html=True)

    # Heading
    st.markdown("""
    <div class="hsu-header">
      <h1>Horizon State University</h1>
      <div class="hsu-subtitle">Advisor Portal</div>
    </div>
    """, unsafe_allow_html=True)

    # Centered logo
    logo_path = Path("templates/img/logo.png")
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if logo_path.exists():
            # Responsive width inside central column; looks good on desktop and mobile
            st.image(str(logo_path), use_column_width=True)
        else:
            st.markdown(
                "<div style='text-align:center; color:#999; font-size:12px;'>.</div>",
                unsafe_allow_html=True
            )

def render(navigate_to):
    # Header and logo above the form
    _render_header_and_logo()

    # Center the login "card" form
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        st.markdown("""
        <div class='login-title'>
            <h2>🔐 Sign In</h2>
        </div>
        <div class='login-subtitle'>Enter your advisor credentials to continue</div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        sign_in = st.button("Sign in", use_container_width=True)
        if sign_in:
            if username in _USERS and _USERS[username] == password:
                st.session_state['authenticated'] = True
                st.session_state['user'] = username
                st.success("Signed in successfully")
                # redirect to home (navigate_to triggers rerun)
                navigate_to('institutional')
            else:
                st.error("Invalid credentials")

        st.markdown("<div class='login-footer'>Need help? Contact IT support.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)