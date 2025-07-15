import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

  
def data_analysis():
    st.header("Data Analysis & Hydrate Formation Prediction")
    
    # Import the get_uploaded_datasets function
    from .data_upload import get_uploaded_datasets
    
    # Train the ML model
    st.subheader("Machine Learning Model")
    with st.expander("Model Training Information", expanded=False):
        st.info("The model is trained using final.csv data with features like gas volume, valve position, and rolling statistics to predict hydrate formation likelihood.")
        
        if st.button("Retrain Model"):
            st.cache_resource.clear()
            model, scaler, feature_columns = train_hydrate_model()
        else:
            model, scaler, feature_columns = train_hydrate_model()
    
    # Get uploaded datasets
    uploaded_datasets = get_uploaded_datasets()
    
    if uploaded_datasets:
        # Dataset selection
        st.subheader("Dataset Selection")
        selected_dataset = st.selectbox(
            "Select dataset for analysis:",
            options=list(uploaded_datasets.keys()),
            key="dataset_selector"
        )
        
        if selected_dataset:
            df = uploaded_datasets[selected_dataset].copy()
            
            # Generate predictions
            st.subheader("Hydrate Formation Predictions")
            if model is not None and scaler is not None:
                with st.spinner("Generating predictions..."):
                    predictions = predict_hydrate_likelihood(df, model, scaler, feature_columns)
                    if predictions is not None:
                        df['Predicted_Hydrate_Likelihood'] = predictions
                        
                        # Display prediction statistics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Max Risk", f"{predictions.max():.2f}")
                        with col2:
                            st.metric("Avg Risk", f"{predictions.mean():.2f}")
                        with col3:
                            high_risk_count = np.sum(predictions > 5.0)
                            st.metric("High Risk Points", high_risk_count)
                        with col4:
                            st.metric("Total Points", len(predictions))
                        
                        # Risk alerts
                        if predictions.max() > 7.0:
                            st.error("CRITICAL: Very high hydrate formation risk detected!")
                        elif predictions.max() > 5.0:
                            st.warning("WARNING: High hydrate formation risk detected!")
                        else:
                            st.success("Hydrate formation risk is within acceptable limits")
            
            # Visualization options
            st.subheader("Data Visualization")
            chart_options = [
                "Time Series - All Variables",
                "Correlation Heatmap", 
                "Hydrate Risk Distribution",
                "Valve vs Volume Relationship",
                "Risk Alert Timeline"
            ]
            
            selected_chart = st.selectbox(
                "Select visualization type:",
                options=chart_options,
                key="chart_selector"
            )
            
            # Generate and display the selected chart
            if selected_chart:
                fig = create_visualization(df, selected_chart, selected_dataset)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True)

            # Data table with predictions
            st.subheader("Data Table")
            display_columns = st.multiselect(
                "Select columns to display:",
                options=df.columns.tolist(),
                default=df.columns.tolist()[:5],  # Show first 5 columns by default
                key="column_selector"
            )
            
            if display_columns:
                st.dataframe(df[display_columns], use_container_width=True)
            
            # Export predictions
            st.subheader("Export Results")
            
            # Show what's available for download
            if 'Predicted_Hydrate_Likelihood' in df.columns:
                st.success("Dataset includes ML predictions - ready for download")
                
                # Preview what will be downloaded
                with st.expander("Preview Download Data", expanded=False):
                    st.write(f"**Columns to be included:** {len(df.columns)}")
                    st.write(f"**Rows:** {len(df)}")
                    st.write("**Column Names:**")
                    for i, col in enumerate(df.columns, 1):
                        st.write(f"{i}. {col}")
                
                # Generate CSV data
                try:
                    csv_data = df.to_csv(index=False)
                    
                    # Create download button
                    st.download_button(
                        label="Download data with predictions",
                        data=csv_data,
                        file_name=f"{selected_dataset}_with_predictions.csv",
                        mime="text/csv",
                        help="Download the dataset with ML predictions included"
                    )
                    
                    st.info(f"File will be saved as: {selected_dataset}_with_predictions.csv")
                    
                except Exception as e:
                    st.error(f"Error preparing download: {str(e)}")
                    st.info("Please try selecting the dataset again or contact support.")
                    
            else:
                st.warning("No predictions available for this dataset")
                st.info("Please wait for the ML model to generate predictions, then try again.")
                
                # Still offer to download original data
                if st.button("Download original data (without predictions)"):
                    try:
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="Download original data",
                            data=csv_data,
                            file_name=f"{selected_dataset}_original.csv",
                            mime="text/csv",
                            help="Download the original dataset without predictions"
                        )
                    except Exception as e:
                        st.error(f"Error preparing download: {str(e)}")
        
        # Manage Datasets section
        st.subheader("Manage Datasets")
        col1 = st.columns(1)[0]
        
        with col1:
            if uploaded_datasets:
                dataset_to_remove = st.selectbox(
                    "Select dataset to remove",
                    options=list(uploaded_datasets.keys()),
                    key="remove_dataset_analysis"
                )
                
                if st.button("Remove Dataset"):
                    if dataset_to_remove in st.session_state.uploaded_datasets:
                        del st.session_state.uploaded_datasets[dataset_to_remove]
                        if 'remove_dataset_analysis' in st.session_state:
                            del st.session_state['remove_dataset_analysis']
                        st.success(f"Removed {dataset_to_remove}")
                        st.rerun()
    
    else:
        st.warning("No datasets uploaded yet. Please upload CSV files in the Data Upload page to proceed.")
        st.info("**Tip**: Upload your pipeline data CSV files to get started with hydrate formation analysis and predictions!")

# Machine Learning Functions
@st.cache_data
def load_training_data():
    """Load the training data from final.csv"""
    try:
        # Get the path to the data folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, '..', '..', 'data', 'final.csv')
        
        df = pd.read_csv(data_path)
        df['Time'] = pd.to_datetime(df['Time'])
        return df
    except Exception as e:
        st.error(f"Error loading training data: {str(e)}")
        return None

@st.cache_resource
def train_hydrate_model():
    """Train the hydrate formation prediction model"""
    df = load_training_data()
    if df is None:
        return None, None, None
    
    # Feature engineering
    df['Volume_Diff'] = df['Inj Gas Meter Volume Instantaneous'] - df['Inj Gas Meter Volume Setpoint']
    df['Volume_Ratio'] = df['Inj Gas Meter Volume Instantaneous'] / df['Inj Gas Meter Volume Setpoint']
    df['Hour'] = df['Time'].dt.hour
    df['Day'] = df['Time'].dt.day
    
    # Select features for training
    feature_columns = [
        'Inj Gas Meter Volume Instantaneous',
        'Inj Gas Meter Volume Setpoint',
        'Inj Gas Valve Percent Open',
        'Rolling Std',
        'Volume_Diff',
        'Volume_Ratio',
        'Hour',
        'Day'
    ]
    
    X = df[feature_columns].fillna(0)
    y = df['Likelihood of Hydrate']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    st.success(f"Model trained successfully! MSE: {mse:.4f}, R²: {r2:.4f}")
    
    return model, scaler, feature_columns

def predict_hydrate_likelihood(df, model, scaler, feature_columns):
    """Predict hydrate formation likelihood for uploaded data"""
        
    if model is None or scaler is None:
        return None
    
    # Feature engineering (same as training)
    df_processed = df.copy()
    df_processed['Volume_Diff'] = df_processed['Inj Gas Meter Volume Instantaneous'] - df_processed['Inj Gas Meter Volume Setpoint']
    df_processed['Volume_Ratio'] = df_processed['Inj Gas Meter Volume Instantaneous'] / df_processed['Inj Gas Meter Volume Setpoint']
    
    # Handle time features if Time column exists
    if 'Time' in df_processed.columns:
        df_processed['Time'] = pd.to_datetime(df_processed['Time'])
        df_processed['Hour'] = df_processed['Time'].dt.hour
        df_processed['Day'] = df_processed['Time'].dt.day
    else:
        df_processed['Hour'] = 0
        df_processed['Day'] = 1
    
    # Add Rolling Std if not present
    if 'Rolling Std' not in df_processed.columns:
        df_processed['Rolling Std'] = df_processed['Inj Gas Meter Volume Instantaneous'].rolling(window=5).std().fillna(0)
    
    # Select features and predict
    X = df_processed[feature_columns].fillna(0)
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    
    return predictions

def create_visualization(df, chart_type, dataset_name):
    """Create different types of visualizations"""
    fig = None
    
    if chart_type == "Time Series - All Variables":
        # Check if we have the required columns
        required_cols = ['Inj Gas Meter Volume Instantaneous', 'Inj Gas Meter Volume Setpoint', 'Inj Gas Valve Percent Open']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"Missing required columns for time series: {missing_cols}")
            st.info(f"Available columns: {list(df.columns)}")
            return None
        
        # Create subplots - simplified version
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Volume Instantaneous', 'Volume Setpoint', 'Valve Percent Open', 'Hydrate Likelihood'),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Prepare time data
        if 'Time' in df.columns:
            try:
                time_data = pd.to_datetime(df['Time'])
            except:
                time_data = df.index
        else:
            time_data = df.index
        
        # Add traces with error handling
        try:
            fig.add_trace(go.Scatter(x=time_data, y=df['Inj Gas Meter Volume Instantaneous'], 
                                    name='Volume Instantaneous', line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(x=time_data, y=df['Inj Gas Meter Volume Setpoint'], 
                                    name='Volume Setpoint', line=dict(color='red')), row=1, col=2)
            fig.add_trace(go.Scatter(x=time_data, y=df['Inj Gas Valve Percent Open'], 
                                    name='Valve % Open', line=dict(color='green')), row=2, col=1)
            
            if 'Predicted_Hydrate_Likelihood' in df.columns:
                fig.add_trace(go.Scatter(x=time_data, y=df['Predicted_Hydrate_Likelihood'], 
                                        name='Predicted Hydrate Likelihood', line=dict(color='orange')), row=2, col=2)
            else:
                # Add a placeholder or empty plot
                fig.add_trace(go.Scatter(x=time_data, y=[0]*len(time_data), 
                                        name='No Predictions Available', line=dict(color='gray')), row=2, col=2)
            
            fig.update_layout(height=600, title_text=f"Time Series Analysis - {dataset_name}", showlegend=True)
            
        except Exception as e:
            st.error(f"Error creating time series plot: {str(e)}")
            return None
        
    elif chart_type == "Correlation Heatmap":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(corr_matrix, 
                       text_auto=True, 
                       aspect="auto",
                       title=f"Correlation Matrix - {dataset_name}")
        
    elif chart_type == "Hydrate Risk Distribution":
        if 'Predicted_Hydrate_Likelihood' in df.columns:
            fig = px.histogram(df, x='Predicted_Hydrate_Likelihood', 
                             title=f"Hydrate Risk Distribution - {dataset_name}",
                             nbins=30)
        else:
            st.warning("No hydrate predictions available for this dataset")
            return None
            
    elif chart_type == "Valve vs Volume Relationship":
        fig = px.scatter(df, x='Inj Gas Valve Percent Open', y='Inj Gas Meter Volume Instantaneous',
                        color='Predicted_Hydrate_Likelihood' if 'Predicted_Hydrate_Likelihood' in df.columns else None,
                        title=f"Valve vs Volume Relationship - {dataset_name}")
        
    elif chart_type == "Risk Alert Timeline":
        if 'Predicted_Hydrate_Likelihood' in df.columns:
            high_risk_threshold = 5.0
            df['Risk_Level'] = df['Predicted_Hydrate_Likelihood'].apply(
                lambda x: 'High' if x > high_risk_threshold else 'Medium' if x > 2.0 else 'Low'
            )
            
            time_col = 'Time' if 'Time' in df.columns else df.index
            fig = px.line(df, x=time_col, y='Predicted_Hydrate_Likelihood',
                         color='Risk_Level',
                         title=f"Hydrate Risk Timeline - {dataset_name}")
            fig.add_hline(y=high_risk_threshold, line_dash="dash", line_color="red",
                         annotation_text="High Risk Threshold")
        else:
            st.warning("No hydrate predictions available for this dataset")
            return None
    
    return fig

def create_matplotlib_visualization(df, chart_type, dataset_name):
    """Create matplotlib-based visualizations as fallback"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if chart_type == "Time Series - All Variables":
        # Check if we have the required columns
        required_cols = ['Inj Gas Meter Volume Instantaneous', 'Inj Gas Meter Volume Setpoint', 'Inj Gas Valve Percent Open']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"Missing required columns for time series: {missing_cols}")
            st.info(f"Available columns: {list(df.columns)}")
            return None
        
        # Prepare time data
        if 'Time' in df.columns:
            try:
                time_data = pd.to_datetime(df['Time'])
            except:
                time_data = df.index
        else:
            time_data = df.index
        
        try:
            ax.plot(time_data, df['Inj Gas Meter Volume Instantaneous'], label='Volume Instantaneous', color='blue')
            ax.plot(time_data, df['Inj Gas Meter Volume Setpoint'], label='Volume Setpoint', color='red', linestyle='--')
            ax.plot(time_data, df['Inj Gas Valve Percent Open'], label='Valve % Open', color='green')
            
            if 'Predicted_Hydrate_Likelihood' in df.columns:
                ax2 = ax.twinx()
                ax2.plot(time_data, df['Predicted_Hydrate_Likelihood'], label='Hydrate Likelihood', color='orange')
                ax2.set_ylabel('Hydrate Likelihood')
                ax2.legend(loc='upper right')
            
            ax.set_title(f'Time Series Analysis - {dataset_name}')
            ax.set_xlabel('Time')
            ax.set_ylabel('Values')
            ax.legend()
            ax.grid(True)
            
        except Exception as e:
            st.error(f"Error creating matplotlib time series plot: {str(e)}")
            return None
        
    elif chart_type == "Correlation Heatmap":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr_matrix.columns)
        ax.set_title(f'Correlation Matrix - {dataset_name}')
        plt.colorbar(im, ax=ax)
        
    elif chart_type == "Hydrate Risk Distribution":
        if 'Predicted_Hydrate_Likelihood' in df.columns:
            ax.hist(df['Predicted_Hydrate_Likelihood'], bins=30, alpha=0.7, color='orange')
            ax.set_title(f'Hydrate Risk Distribution - {dataset_name}')
            ax.set_xlabel('Predicted Hydrate Likelihood')
            ax.set_ylabel('Frequency')
        else:
            st.warning("No hydrate predictions available for this dataset")
            return None
            
    elif chart_type == "Valve vs Volume Relationship":
        scatter = ax.scatter(df['Inj Gas Valve Percent Open'], df['Inj Gas Meter Volume Instantaneous'],
                           c=df['Predicted_Hydrate_Likelihood'] if 'Predicted_Hydrate_Likelihood' in df.columns else 'blue',
                           cmap='Reds', alpha=0.7)
        ax.set_title(f'Valve vs Volume Relationship - {dataset_name}')
        ax.set_xlabel('Valve Percent Open')
        ax.set_ylabel('Volume Instantaneous')
        if 'Predicted_Hydrate_Likelihood' in df.columns:
            plt.colorbar(scatter, ax=ax, label='Hydrate Likelihood')
        
    elif chart_type == "Risk Alert Timeline":
        if 'Predicted_Hydrate_Likelihood' in df.columns:
            time_col = 'Time' if 'Time' in df.columns else df.index
            if 'Time' in df.columns:
                time_data = pd.to_datetime(df['Time'])
            else:
                time_data = df.index
                
            ax.plot(time_data, df['Predicted_Hydrate_Likelihood'], color='orange', linewidth=2)
            ax.axhline(y=5.0, color='red', linestyle='--', label='High Risk Threshold')
            ax.set_title(f'Hydrate Risk Timeline - {dataset_name}')
            ax.set_xlabel('Time')
            ax.set_ylabel('Hydrate Likelihood')
            ax.legend()
            ax.grid(True)
        else:
            st.warning("No hydrate predictions available for this dataset")
            return None
    
    plt.tight_layout()
    return fig