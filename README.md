# Smart Parking Analytics

## Project Overview
Smart Parking Analytics is a data engineering
project that analyzes parking occupancy data
to understand parking usage and peak hours.

## Objectives
- Clean parking datasets.
- Remove duplicate and invalid records.
- Analyze parking occupancy.
- Identify peak parking hours.
- Display insights using a dashboard.

## Technologies Used
- Python
- Pandas
- SQLite
- Streamlit
- Matplotlib

## Dataset Results
- Original Records: 35,717
- Cleaned Records: 35,116
- Parking Areas: 30
- Average Occupancy: 48.98%

## Data Quality
- Duplicates before cleaning: 216
- Duplicates after cleaning: 0
- Missing values after cleaning: 0
- Records removed: 601

## How to Run

1. Install required libraries:
   pip install pandas matplotlib streamlit sqlalchemy

2. Run the data pipeline:
   python main.py

3. Run the dashboard:
   streamlit run dashboard.py

## Database
SQLite database:
outputs/parking_analysis.db

## Dashboard
The dashboard displays parking statistics,
parking area analysis and peak hour analysis.