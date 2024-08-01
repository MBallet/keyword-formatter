import streamlit as st
import pandas as pd
import numpy as np

# Load the CSV file
uploaded_file = st.file_uploader("Choose a file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Process the data
    # Extract necessary columns and rename them accordingly
    df = data[['Keyword', 'Volume', 'Trend', 'Keyword Difficulty']].copy()
    df.rename(columns={'Volume': 'Average Monthly Search Volume', 'Keyword Difficulty': 'Difficulty'}, inplace=True)
    
    # Calculate three-month difference and YoY change from 'Trend' column
    trend_data = df['Trend'].str.split(',', expand=True).astype(float)
    df['Three Month Difference'] = trend_data.iloc[:, -1] - trend_data.iloc[:, -4]
    df['YoY Change'] = trend_data.iloc[:, -1] - trend_data.iloc[:, 0]
    
    # Add 'Current Rank' and 'Category' columns
    df['Current Rank'] = np.nan
    df['Category'] = ''
    
    # Color coding for 'Average Monthly Search Volume'
    def color_code(val):
        if val < 100:
            color = 'red'
        elif val < 1000:
            color = 'yellow'
        else:
            color = 'green'
        return f'background-color: {color}'

    # Applying color code to the 'Average Monthly Search Volume' column
    styled_df = df.style.applymap(color_code, subset=['Average Monthly Search Volume'])
    
    # Display the formatted dataframe
    st.dataframe(styled_df)
    
    # Provide an option to download the formatted dataframe as a CSV file
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download formatted data as CSV",
        data=csv,
        file_name='formatted_data.csv',
        mime='text/csv',
    )
