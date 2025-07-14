import streamlit as st
from . import style

def landing_page():
    # Custom CSS for enhanced styling
    style.style()
    
    # Main header with enhanced styling
    st.markdown("<h1 class='main-header'>Hydrate Alert</h1>", unsafe_allow_html=True)
    
    # Welcome message and description
    st.markdown("""
    <div class='welcome-section'>
        <h3>Industrial Gas Injection Monitoring System</h3>
        <p style='font-size: 18px; margin: 20px 0;'>
            Advanced monitoring solution designed to detect potential hydrate formation in gas injection systems. 
            Prevent costly system failures and pipeline blockages with data analysis and intelligent alerting.
        </p>
        <div class='alert-badge'>Mission Critical System Protection</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section with enhanced cards
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h4 style='color: #1f4e79; margin-bottom: 30px;'>Core Capabilities</h4>
        <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 20px;'>
            <div class='feature-card' style='flex: 1; min-width: 250px; max-width: 300px;'>
                <h5 style='color: #667eea;'>Time-Series Data Processing</h5>
                <p style='color: #555;'>Upload and analyze CSV data from gas injection systems with comprehensive trend analysis</p>
            </div>
            <div class='feature-card' style='flex: 1; min-width: 250px; max-width: 300px;'>
                <h5 style='color: #667eea;'>Volume & Valve Monitoring</h5>
                <p style='color: #555;'>Real-time visualization of gas volume trends and valve settings for operational insights</p>
            </div>
            <div class='feature-card' style='flex: 1; min-width: 250px; max-width: 300px;'>
                <h5 style='color: #667eea;'>Hydrate Risk Detection</h5>
                <p style='color: #555;'>Intelligent alerts for significant volume drops indicating potential hydrate formation</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login instruction with enhanced styling
    st.markdown("<div class='login-box'>Please use the sidebar to login and access the monitoring system</div>", unsafe_allow_html=True)