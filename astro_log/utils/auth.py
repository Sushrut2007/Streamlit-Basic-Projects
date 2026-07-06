import streamlit as st
from supabase import create_client, Client
from supabase_auth.errors import AuthApiError
import pandas as pd


@st.cache_resource(show_spinner='...Initiating auth connection')
def init_connection():
    """
    Make database connection.
    """

    url = st.secrets['supabase_url']
    key = st.secrets['supabase_publishable_key']

    return create_client(url, key)
#------------------------------------------------------------------


def sign_up(supabase, email, password):
    """
    Create a new user account if email already doesn't exists.
    """
    
    session = supabase.auth.sign_up({
        'email': email,
        'password': password
    })

    return session
#------------------------------------------------------------------



def sign_in(supabase, email, password):
    """
    Sign in user.
    """

    session = supabase.auth.sign_in_with_password({
        'email': email,
        'password': password
    })

    return session
#------------------------------------------------------------------


def sign_out(supabase):
    """
    Sign out the user.
    """
    try:
        supabase.auth.sign_out()
        return True

    except AuthApiError:
        return False