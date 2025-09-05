# Outlier Earnings Analyzer

A Streamlit application for analyzing and visualizing earnings data from Outlier.

## Features

- Analyzes earnings data from CSV files
- Visualizes earnings across different projects
- Shows time spent on various projects
- Categorizes income (rewards, platform earnings, assessments)
- Interactive data upload capability

## How to Run Locally

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run earnings_analyzer/app.py
   ```

## Data Format Requirements

The CSV file should contain the following columns:
- workDate
- duration
- payout
- payType
- projectName

## Deployment

This app is deployed on Streamlit Cloud and can be accessed at: [Your App URL]
