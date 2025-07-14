import streamlit as st

def style():
    st.markdown("""
    <style>
    .main-header {
        text-align: center; 
        margin-top: -50px; 
        padding-top: 0px;
        color: #1f4e79;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .welcome-section {
        text-align: center; 
        margin-top: 30px;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 10px;
        transition: transform 0.3s ease;
        border-left: 4px solid #667eea;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .login-box {
        text-align: center; 
        font-size: 16px; 
        margin-top: 40px; 
        padding: 25px; 
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        border-radius: 15px;
        border: 2px solid #e17055;
        color: #2d3436;
        font-weight: 500;
    }
    .alert-badge {
        background: #e74c3c;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }
    """, unsafe_allow_html=True)

def google_button_style():
    st.markdown("""
            <style>
            .google-login-container {
                margin: 10px 0;
            }
            .google-login-btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: #ffffff;
                color: #3c4043;
                border: 1px solid #dadce0;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
                width: 100%;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .google-login-btn:hover {
                background-color: #f8f9fa;
                border-color: #c6c8ca;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                color: #3c4043;
                text-decoration: none;
            }
            .google-logo {
                width: 18px;
                height: 18px;
                margin-right: 12px;
            }
            </style>
            """, unsafe_allow_html=True)