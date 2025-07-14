# Hydrate Alert - HACKUTD Fall 2024


- Web application designed to monitor gas injection systems and detect potential hydrate formation, which can lead to system failures or pipeline blockages.
- The app processes time-series data uploaded by users in CSV format.
- Visualizes trends in gas volume and valve settings, and alerts operators when significant volume drops occur, indicating a potential hydrate risk.    

-----

```
# Ran using virtual python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```
