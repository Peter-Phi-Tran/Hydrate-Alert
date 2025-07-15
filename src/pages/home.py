import streamlit as st
from . import style

def home_page():
    # Apply custom styling
    style.style()
    # Welcome section
    st.markdown("""
    <div class='welcome-section'>
        <h3>Welcome to Hydrate Alert System</h3>
        <p style='font-size: 18px; margin: 20px 0;'>
            Your comprehensive pipeline monitoring solution is ready. Monitor gas injection systems, 
            analyze data trends, and receive intelligent alerts for potential hydrate formation.
        </p>
        <div class='alert-badge'>System Status: Online</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats Section
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h4 style='color: #1f4e79; margin-bottom: 30px;'>System Overview</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Display system stats
    col1, col2, col3, col4 = st.columns(4)

    # Get uploaded datasets info
    from .data_upload import get_uploaded_datasets
    uploaded_datasets = get_uploaded_datasets()

    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.metric(
            label=" Datasets Uploaded",
            value=len(uploaded_datasets),
            help="Total number of datasets currently loaded"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        total_rows = sum(df.shape[0] for df in uploaded_datasets.values()) if uploaded_datasets else 0
        st.metric(
            label=" Data Points",
            value=f"{total_rows:,}",
            help="Total number of data points across all datasets"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        total_size = sum(df.memory_usage(deep=True).sum() for df in uploaded_datasets.values()) if uploaded_datasets else 0
        size_mb = total_size / (1024 * 1024)
        st.metric(
            label=" Memory Usage",
            value=f"{size_mb:.1f} MB",
            help="Total memory usage of uploaded datasets"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.metric(
            label=" ML Model",
            value="Active",
            help="Machine learning model status"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Actions Section
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h4 style='color: #1f4e79; margin-bottom: 30px;'>Quick Actions</h4>
        <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 20px;'>
            <div class='feature-card' style='flex: 1; min-width: 250px; max-width: 300px;'>
                <h5 style='color: #667eea;'>Upload New Data</h5>
                <p style='color: #555;'>Upload CSV files containing pipeline data for analysis and monitoring</p>
            </div>
            <div class='feature-card' style='flex: 1; min-width: 250px; max-width: 300px;'>
                <h5 style='color: #667eea;'>Analyze Data</h5>
                <p style='color: #555;'>View predictions, visualizations, and detailed analysis of your pipeline data</p>
            </div>
            <div class='feature-card' style='flex: 1; min-width: 250px; max-width: 300px;'>
                <h5 style='color: #667eea;'>Get Help</h5>
                <p style='color: #555;'>Access documentation, FAQs, and troubleshooting guides</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recent Activity Section
    if uploaded_datasets:
        st.markdown("""
        <div style='text-align: center; margin: 40px 0;'>
            <h4 style='color: #1f4e79; margin-bottom: 30px;'>Recent Datasets</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Show recent datasets in a nice format
        for name, df in list(uploaded_datasets.items())[:3]:  # Show only first 3
            with st.expander(f"{name}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                    st.write(f"**Rows:** {df.shape[0]:,}")
                    st.markdown("</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                    st.write(f"**Columns:** {df.shape[1]}")
                    st.markdown("</div>", unsafe_allow_html=True)
                with col3:
                    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
                    st.write(f"**Size:** {memory_mb:.1f} MB")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Show column names
                st.write("**Columns:** " + ", ".join(df.columns.tolist()))
        
        # Show more datasets message if there are more than 3
        if len(uploaded_datasets) > 3:
            st.info(f"And {len(uploaded_datasets) - 3} more datasets available in Data Analysis page")
    
    # System Health Section
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h4 style='color: #1f4e79; margin-bottom: 30px;'>System Health</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # System status indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='text-align: center;'>
            <h5 style='color: #27ae60;'>Data Processing</h5>
            <p style='color: #555;'>All systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='text-align: center;'>
            <h5 style='color: #27ae60;'>ML Engine</h5>
            <p style='color: #555;'>Model ready for predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card' style='text-align: center;'>
            <h5 style='color: #27ae60;'>Visualization</h5>
            <p style='color: #555;'>Charts and graphs available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation Instructions
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h4 style='color: #1f4e79; margin-bottom: 30px;'>Navigation Guide</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation steps
    st.markdown("""
    <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; margin-top: 20px;'>
        <div class='feature-card' style='flex: 1; min-width: 200px; max-width: 240px; text-align: center;'>
            <h6 style='color: #667eea;'>Step 1</h6>
            <p style='color: #555;'>Upload your CSV data files</p>
        </div>
        <div class='feature-card' style='flex: 1; min-width: 200px; max-width: 240px; text-align: center;'>
            <h6 style='color: #667eea;'>Step 2</h6>
            <p style='color: #555;'>Let ML model analyze your data</p>
        </div>
        <div class='feature-card' style='flex: 1; min-width: 200px; max-width: 240px; text-align: center;'>
            <h6 style='color: #667eea;'>Step 3</h6>
            <p style='color: #555;'>View predictions and insights</p>
        </div>
        <div class='feature-card' style='flex: 1; min-width: 200px; max-width: 240px; text-align: center;'>
            <h6 style='color: #667eea;'>Step 4</h6>
            <p style='color: #555;'>Export results for action</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer with tips
    st.markdown("""
    <div class='login-box' style='margin-top: 50px;'>
     <strong>Pro Tip:</strong> Upload multiple datasets to compare pipeline performance across different time periods or locations.
        Use the Data Analysis page to generate comprehensive reports and identify trends.
    </div>
    """, unsafe_allow_html=True)