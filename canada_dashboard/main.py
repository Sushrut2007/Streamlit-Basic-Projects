import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "data/quarterly_canada_population.csv"

df = pd.read_csv(path, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})

st.title('Population of Canada')

with st.expander('See full table'):
    st.write(df)

# Extract the quarter (Q1, Q2, etc.) and year as a seperate columns
df[['Q', 'Year']] = df['Quarter'].str.split(expand=True)
df['Year'] = df['Year'].astype(int) # Convert year to integer


with st.form("Canada form"): 
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write('Choose a starting date')
        start_Q = st.selectbox('Start quarter', options=sorted(df['Q'].unique()))
        starting_date = st.slider(
            label = "Start Year", 
            min_value = df['Year'].min(),
            max_value = df['Year'].max())
    
    with col2:
        st.write('Choose an end date')
        end_Q = st.selectbox('End quarter', options=sorted(df['Q'].unique()))
        end_date = st.slider(
            label = "End year", 
            min_value = df['Year'].min(),
            max_value = df['Year'].max())
        
    with col3:
        st.write('Choose a location')
        location = st.selectbox('Choose a location', options=df.columns[1:-2])
        
    button = st.form_submit_button('Analyze')
