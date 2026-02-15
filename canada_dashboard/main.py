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
        starting_year = st.slider(
            label = "Start Year", 
            min_value = df['Year'].min(),
            max_value = df['Year'].max())
    
    with col2:
        st.write('Choose an end date')
        end_Q = st.selectbox('End quarter', options=sorted(df['Q'].unique()))
        end_year = st.slider(
            label = "End year", 
            min_value = df['Year'].min(),
            max_value = df['Year'].max())
        
    with col3:
        st.write('Choose a location')
        location = st.selectbox('Choose a location', options=df.columns[1:-2])

    button = st.form_submit_button('Analyze')

# Output section
if button:
    tab1, tab2 = st.tabs(['Population change', 'Compare'])
    # Tab 1 contents
    with tab1:
        st.header(f'Population change from {start_Q} {starting_year} to {end_Q} {end_year}')

        col1, col2 = st.columns(2)
        with col1:
            # Create mask targeting starting population
            start_mask = (df['Q'] == start_Q) & (df['Year']==starting_year)
            start_pop_value = df.loc[start_mask, location].iloc[0]
            st.metric(f'{start_Q} {starting_year}', value=start_pop_value)

            # Create mask targeting ending population
            end_mask = (df['Q'] == end_Q) & (df['Year'] == end_year)
            end_pop_value = df.loc[end_mask, location].iloc[0]
            diff = (end_pop_value - start_pop_value) / start_pop_value * 100
            st.metric(f'{end_Q} {end_year}', value=end_pop_value, delta=f'{diff:.2f}%')

        with col2:
            start_row = df[start_mask].index[0] # Retrieve the index of the start row
            end_row = df[end_mask].index[0] # Retrieve the index of the start row
            df_trend = df.iloc[min(start_row, end_row) : max(start_row, end_row) + 1]
            fig, ax = plt.subplots()
            ax.plot(df_trend['Quarter'], df_trend[location])
            
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([df_trend['Quarter'].iloc[0], df_trend['Quarter'].iloc[-1]])
            st.pyplot(fig)

