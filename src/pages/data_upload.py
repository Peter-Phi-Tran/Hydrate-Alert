import streamlit as st
import pandas as pd
from typing import Dict, List

def upload_data():
    st.header("Upload Your Pipeline Data")
    
    # Initialize session state for storing uploaded data
    if 'uploaded_datasets' not in st.session_state:
        st.session_state.uploaded_datasets = {}
    
    # Create tabs for different upload methods
    tab1, tab2 = st.tabs(["Single Upload", "Batch Upload"])
    
    with tab1:
        st.subheader("Upload Individual Pipeline Data")
        
        # Pipeline name input
        pipeline_name = st.text_input("Pipeline Name", placeholder="Enter pipeline identifier")
        
        # File uploader for single file
        uploaded_file = st.file_uploader(
            "Choose a CSV file", 
            type=['csv'],
            key="single_upload"
        )
        
        if uploaded_file and pipeline_name:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_datasets[pipeline_name] = df
                st.success(f"Successfully uploaded data for {pipeline_name}")
                st.dataframe(df.head())
                st.info(f"Dataset shape: {df.shape}")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        elif uploaded_file and not pipeline_name:
            st.warning("Please enter a pipeline name.")
    
    with tab2:
        st.subheader("Upload Multiple Pipeline Files")
        
        # Multiple file uploader
        uploaded_files = st.file_uploader(
            "Choose CSV files", 
            type=['csv'],
            accept_multiple_files=True,
            key="batch_upload"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Extract pipeline name from filename (remove .csv extension)
                pipeline_name = uploaded_file.name.replace('.csv', '')
                
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.uploaded_datasets[pipeline_name] = df
                        
                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {str(e)}")
            
            st.success(f"Successfully processed {len(uploaded_files)} files please hold.")
    
    # Display summary of uploaded datasets
    if st.session_state.uploaded_datasets:
        st.subheader("Uploaded Datasets Summary")
        
        # Create summary table
        summary_data = []
        for name, df in st.session_state.uploaded_datasets.items():
            summary_data.append({
                'Pipeline': name,
                'Rows': df.shape[0],
                'Columns': df.shape[1],
                'Memory Usage (MB)': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df)
        
        # Export combined data option
        if len(st.session_state.uploaded_datasets) > 1:
            st.subheader("Export Combined Dataset Info")
            combined_info = get_combined_dataset_info(st.session_state.uploaded_datasets)
            if st.download_button(
                label="Download Combined Dataset Info",
                data=combined_info.to_csv(index=False),
                file_name="combined_pipeline_info.csv",
                mime="text/csv"
            ):
                st.success("Download started!")
    else:
        st.info("No datasets uploaded yet. Please upload CSV files to proceed.")

def get_combined_dataset_info(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create a summary of all uploaded datasets"""
    info_data = []
    
    for name, df in datasets.items():
        # Get column info
        for col in df.columns:
            info_data.append({
                'Pipeline': name,
                'Column': col,
                'Data Type': str(df[col].dtype),
                'Non-Null Count': df[col].count(),
                'Null Count': df[col].isnull().sum(),
                'Unique Values': df[col].nunique()
            })
    
    return pd.DataFrame(info_data)

# Function to get uploaded datasets (for use in other modules)
def get_uploaded_datasets() -> Dict[str, pd.DataFrame]:
    """Return the uploaded datasets from session state"""
    return st.session_state.get('uploaded_datasets', {})
