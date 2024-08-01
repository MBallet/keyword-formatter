import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import xlsxwriter

# Function to color code the Excel file
def color_code_excel(writer, df):
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Define a format for the header
    header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D7E4BC', 'border': 1})

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Apply color coding for 'Average Monthly Search Volume'
    for row_num, value in enumerate(df['Average Monthly Search Volume'], start=1):
        if value < 100:
            color = '#FF9999'  # red
        elif value < 1000:
            color = '#FFFF99'  # yellow
        else:
            color = '#99FF99'  # green
        worksheet.write(row_num, df.columns.get_loc('Average Monthly Search Volume'), value, workbook.add_format({'bg_color': color}))

# Streamlit app
st.title("SEMRush Data Formatter")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Process the data
    df = data[['Keyword', 'Volume', 'Trend', 'Keyword Difficulty']].copy()
    df.rename(columns={'Volume': 'Average Monthly Search Volume', 'Keyword Difficulty': 'Difficulty'}, inplace=True)
    
    trend_data = df['Trend'].str.split(',', expand=True).astype(float)
    df['Three Month Difference'] = trend_data.iloc[:, -1] - trend_data.iloc[:, -4]
    df['YoY Change'] = trend_data.iloc[:, -1] - trend
