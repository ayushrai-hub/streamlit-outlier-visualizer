"""
Streamlit app for Outlier Earnings Report Analysis.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils.earnings_utils import parse_duration, format_seconds

def analyze_earnings_report(df):
    """Analyze earnings report DataFrame and display results/visualizations in Streamlit."""
    try:
        # Data Cleaning and Preprocessing
        df['workDate'] = pd.to_datetime(df['workDate'], format='mixed', errors='coerce')
        initial_rows = len(df)
        df.dropna(subset=['workDate'], inplace=True)
        if len(df) < initial_rows:
            st.warning(f"Removed {initial_rows - len(df)} rows due to unparseable 'workDate' entries.")
        df['payout'] = df['payout'].replace({'\\$': '', '-': '0'}, regex=True).astype(float)
        df['duration_seconds'] = df['duration'].apply(parse_duration)

        # Calculations
        project_earnings_timeline = df.groupby(['projectName', 'workDate'])['payout'].sum().reset_index()
        total_earnings_per_project = df.groupby('projectName')['payout'].sum().reset_index().sort_values(by='payout', ascending=False)
        total_time_per_project_seconds = df.groupby('projectName')['duration_seconds'].sum().reset_index()
        total_time_per_project_seconds['formatted_duration'] = total_time_per_project_seconds['duration_seconds'].apply(format_seconds)
        total_time_per_project_seconds = total_time_per_project_seconds.sort_values(by='duration_seconds', ascending=False)
        overall_total_time_seconds = df['duration_seconds'].sum()
        overall_total_time_formatted = format_seconds(overall_total_time_seconds)
        rewards_df = df[df['payType'] == 'missionReward']
        total_rewards_money = rewards_df['payout'].sum()
        total_rewards_time = rewards_df['duration_seconds'].sum()
        total_rewards_time_formatted = format_seconds(total_rewards_time)
        other_platform_earnings_df = df[df['payType'] == 'hubstaffOperation']
        total_other_platform_money = other_platform_earnings_df['payout'].sum()
        total_other_platform_time = other_platform_earnings_df['duration_seconds'].sum()
        total_other_platform_time_formatted = format_seconds(total_other_platform_time)
        assessment_df = df[df['projectName'].str.contains('training|screening', case=False, na=False)]
        total_assessment_money = assessment_df['payout'].sum()
        total_assessment_time = assessment_df['duration_seconds'].sum()
        total_assessment_time_formatted = format_seconds(total_assessment_time)

        # Visualizations
        st.subheader("Visualizations")
        project_earnings_timeline_filtered = project_earnings_timeline[project_earnings_timeline['projectName'] != '-']
        if not project_earnings_timeline_filtered.empty:
            fig1, ax1 = plt.subplots(figsize=(15, 7))
            sns.lineplot(data=project_earnings_timeline_filtered, x='workDate', y='payout', hue='projectName', marker='o', ax=ax1)
            ax1.set_title('Money Made on Each Project Over Time')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Payout ($)')
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(True)
            plt.tight_layout()
            st.pyplot(fig1)
        else:
            st.write("No project earnings data available for timeline visualization.")
        if not total_earnings_per_project.empty:
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            sns.barplot(x='payout', y='projectName', data=total_earnings_per_project.head(10), palette='viridis', ax=ax2)
            ax2.set_title('Total Payout per Project (Top 10)')
            ax2.set_xlabel('Total Payout ($)')
            ax2.set_ylabel('Project Name')
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.write("No project payout data available for visualization.")
        if not total_time_per_project_seconds.empty:
            fig3, ax3 = plt.subplots(figsize=(12, 6))
            sns.barplot(x='duration_seconds', y='projectName', data=total_time_per_project_seconds.head(10), palette='magma', ax=ax3)
            ax3.set_title('Total Time Worked per Project (Top 10)')
            ax3.set_xlabel('Total Time Worked (Seconds)')
            ax3.set_ylabel('Project Name')
            plt.tight_layout()
            st.pyplot(fig3)
        else:
            st.write("No project time data available for visualization.")

        # Display Calculated Results
        st.subheader("Calculated Results")
        st.write("### Total Earnings per Project:")
        st.dataframe(total_earnings_per_project)
        st.write("### Total Time Worked per Project:")
        st.dataframe(total_time_per_project_seconds[['projectName', 'formatted_duration']])
        st.write(f"### Overall Total Time Worked: {overall_total_time_formatted}")
        st.write(f"### Total Mission Reward Money: ${total_rewards_money:.2f}")
        st.write(f"Total Mission Reward Time: {total_rewards_time_formatted}")
        st.write(f"### Total Other Platform Earnings Money: ${total_other_platform_money:.2f}")
        st.write(f"Total Other Platform Earnings Time: {total_other_platform_time_formatted}")
        st.write(f"### Total Assessment Money: ${total_assessment_money:.2f}")
        st.write(f"Total Assessment Time: {total_assessment_time_formatted}")
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")

# --- Streamlit UI ---
st.title("Outlier Earnings Report Analysis")
st.write("""
This application analyzes your 'Outlier_Earnings_Report.csv' file to provide insights into project earnings,
time spent, and categorized income (rewards, other platform earnings, and assessment money).

**To use this application:**
1.  Make sure your 'Outlier_Earnings_Report.csv' file is in the same directory as this script.
2.  Run the application using `streamlit run src/app.py` in your terminal.
""")
uploaded_file = st.file_uploader("Upload your Outlier_Earnings_Report.csv file (optional, if not in the same directory)", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV file uploaded and loaded successfully!")
    analyze_earnings_report(df.copy())
else:
    try:
        df = pd.read_csv('earnings_analyzer/data/Outlier_Earnings_Report.csv')
        st.success("Local 'Outlier_Earnings_Report.csv' loaded successfully!")
        analyze_earnings_report(df.copy())
    except FileNotFoundError:
        st.warning("No file uploaded and 'Outlier_Earnings_Report.csv' not found. Please upload or place the CSV in the correct directory.")
    except pd.errors.EmptyDataError:
        st.error("Error: The CSV file is empty. Please provide a file with data.")
    except KeyError as e:
        st.error(f"Error: Missing expected column in the CSV file: {e}. Required columns: workDate, duration, payout, payType, projectName.")
    except Exception as e:
        st.error(f"An unexpected error occurred during file loading: {e}")
