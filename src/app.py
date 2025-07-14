import streamlit as st
from streamlit_option_menu import option_menu
import urllib.parse

import pages.data_upload as data_upload
import pages.data_analysis as data_analysis
import pages.help as help
import pages.home as home
import pages.landing as landing_page
from pages.style import google_button_style

# Import Google Auth (with fallback if not available)
try:
    from google_auth import GoogleAuth, is_google_auth_configured
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    st.warning("Google authentication libraries not installed. Only local authentication available.")

st.set_page_config(initial_sidebar_state="collapsed")

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'user_picture' not in st.session_state:
    st.session_state.user_picture = ""
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Handle Google OAuth callback
if GOOGLE_AUTH_AVAILABLE:
    query_params = st.query_params
    if 'code' in query_params:
        # Only process if we haven't already processed this code
        if 'oauth_processed' not in st.session_state:
            st.session_state.oauth_processed = True
            
            google_auth = GoogleAuth()
            auth_code = query_params['code']
            user_info = google_auth.authenticate_user(auth_code)
            
            if user_info:
                st.session_state.logged_in = True
                st.session_state.username = user_info['name']
                st.session_state.user_email = user_info['email']
                st.session_state.user_picture = user_info.get('picture', '')
                st.success(f"Welcome, {user_info['name']}!")
                
                # Clear query params and oauth_processed flag
                st.query_params.clear()
                if 'oauth_processed' in st.session_state:
                    del st.session_state.oauth_processed
                
                st.rerun()
            else:
                # Authentication failed, clear the processed flag
                if 'oauth_processed' in st.session_state:
                    del st.session_state.oauth_processed
    
    # Handle OAuth errors
    if 'error' in query_params:
        error_description = query_params.get('error_description', ['Unknown error'])[0]
        st.error(f"OAuth Error: {error_description}")
        st.query_params.clear()
        st.rerun()

# Load Google Fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Sidebar for login
with st.sidebar:
    st.header("Login")
    
    if not st.session_state.logged_in:
        
        # Login form
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True):
                # Simple authentication (you can replace this with your own logic)
                if username and password:
                    if username == "admin" and password == "password":  # Replace with real authentication
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_email = f"{username}@local.dev"
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            if st.button("Register", use_container_width=True):
                st.info("Registration feature coming soon!")
        
        # Google OAuth login button (moved below login/register)
        if GOOGLE_AUTH_AVAILABLE and is_google_auth_configured():
            google_auth = GoogleAuth()
            auth_url = google_auth.get_authorization_url()
            
            # Google Login Button with Streamlit button styling
            google_button_style()

            st.markdown(f'''
            <div class="google-login-container">
                <a href="{auth_url}" class="google-login-btn" target="_self">
                    <svg class="google-logo" viewBox="0 0 24 24">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Continue with Google
                </a>
            </div>
            ''', unsafe_allow_html=True)
        else:
            if GOOGLE_AUTH_AVAILABLE:
                st.markdown("---")
                st.warning("Google authentication not configured. Please set up Google OAuth credentials.")
        
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.markdown("Username: `admin`")
        st.markdown("Password: `password`")
        
    else:
        # User is logged in
        st.success(f"Welcome, {st.session_state.username}!")
        st.markdown("---")
        
        # User info with profile picture if available
        st.subheader("User Profile")
        if st.session_state.user_picture:
            st.image(st.session_state.user_picture, width=60)
        st.write(f"**Name:** {st.session_state.username}")
        if st.session_state.user_email:
            st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Status:** Online")
        
        st.markdown("---")
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_email = ""
            st.session_state.user_picture = ""
            st.rerun()

# Only show main content if user is logged in
if st.session_state.logged_in:
    # 4. Top navbar in main area

    selected = option_menu(
        menu_title=None,
        options=["Home", "Upload Data", "Data Analysis", "Help"],
        icons=["‎", "‎ ", "‎ ", "‎ "],
        orientation="horizontal",
        styles={
            "container": {"padding": "0 !important", "background-color": "#f0f0f0", "border-radius": "10px"},
            "nav-link": {"text-align": "center !important", "font-family": "'Nunito', sans-serif !important", "font-size": "1rem", "color": "#000000", "font-weight": "normal !important", "margin": "0", "padding": "10px 20px", "background-color": "#f0f0f0", "border-radius": "8px"},
            "nav-link-selected": {"text-align": "center !important", "font-family": "'Nunito', sans-serif !important", "background-color": "#ff4444", "color": "#000000", "font-weight": "normal !important", "margin": "0", "padding": "10px 20px", "border-radius": "8px"},
        }
    )

    # 5. Render content based on navbar selection
    if selected == "Home":
        home.home_page()

    elif selected == "Upload Data":
        data_upload.upload_data()

    elif selected == "Data Analysis":
        data_analysis.data_analysis()

    elif selected == "Help":
        help.help_page()

else:
    landing_page.landing_page()
