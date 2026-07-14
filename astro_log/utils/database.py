import streamlit as st
import pandas as pd

@st.cache_data(show_spinner='Fetching profile....')
def fetch_profile(supabase):
    """
    Fetch the user profile from profiles table.
    Returns a dataframe
    """
    
    response = supabase.table('profiles').select('*').eq('id' ,st.session_state['user_id']).execute()
    df = pd.DataFrame(response.data)

    return df


def update_profile(supabase, profile_updates):
    """
    Update user profile.
    """

    supabase.table['profiles'].update(profile_updates).eq('id', st.session_state['user_id']).execute()

