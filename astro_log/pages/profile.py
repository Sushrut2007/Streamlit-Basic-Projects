import streamlit as st
import pandas as pd
from utils.auth import init_connection
from utils.database import fetch_profile, update_profile

supabase =  init_connection()

st.title('Profile')
st.caption('Keep your identity up to date.')

# Fetch user profile and data
profile = fetch_profile(supabase)
name = profile.iloc[0]['name']
location = profile.iloc[0]['location']
experience = profile.iloc[0]['experience']
preferred_telescope = profile.iloc[0]['preferred_telescope']



col1, col2 = st.columns(2)
with col1:
    st.caption('User name')
    st.header(name)
    st.caption('Observing location')
    st.header(location)
    st.caption('📅 Experience')
    st.write(experience)
with col2:
    st.caption('🔭 Preferred telescope')
    st.header(preferred_telescope)
