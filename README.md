# Hydrate Alert

A web application for monitoring gas injection systems and detecting potential hydrate formation that can cause system failures or pipeline blockages.

## Features

- **Data Processing**: Upload and analyze time-series data in CSV format
- **Machine Learning**: Predict hydrate formation likelihood using RandomForestRegressor
- **Visualization**: Interactive charts including time series, correlation heatmaps, and risk distributions
- **Authentication**: Google OAuth integration with persistent login
- **Data Export**: Download analysis results with predictions

## Tech Stack

- **Backend**: Python, Streamlit
- **ML**: scikit-learn, NumPy, Pandas
- **Visualization**: Plotly, Matplotlib
- **Authentication**: Google OAuth 2.0

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run src/app.py
```

## Usage

1. Launch the application and authenticate with Google
2. Upload CSV files with time-series data
3. View data analysis and ML predictions
4. Download results with hydrate formation predictions

## Data Format

CSV files should contain columns for timestamp, gas volume, valve settings, and other relevant parameters for optimal analysis.
