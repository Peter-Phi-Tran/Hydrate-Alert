import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

import pages.data_upload as data_upload
import pages.data_analysis as data_analysis
import pages.help as help
import pages.home as home
import pages.landing as landing

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

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
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            if st.button("Register", use_container_width=True):
                st.info("Registration feature coming soon!")
        
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.markdown("Username: `admin`")
        st.markdown("Password: `password`")
        
    else:
        # User is logged in
        st.success(f"Welcome, {st.session_state.username}!")
        st.markdown("---")
        
        # User info
        st.subheader("User Profile")
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Status:** Online")
        
        st.markdown("---")
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
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
    landing.landing_page()
