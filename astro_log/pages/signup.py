import streamlit as st
from utils.auth import init_connection, sign_up
from time import sleep

# Initiate database connection
supabase = init_connection()

st.title("Create an Account 📝")

# Sign up form
with st.form('Signup_form'):
    username = st.text_input('Username')
    email = st.text_input('Email')
    password = st.text_input('Password (minimum 6 characters) ', type='password')
    confirmed_password = st.text_input('Confirm your password', type='password')

    if st.form_submit_button('Sign up'):
        # Sign up if both passwords match
        if password == confirmed_password:
            user, session = sign_up(supabase, email, password)
            st.success('Sign up successful!', icon='✅')

            # Insert id and username into profiles to create a new profile
            supabase.table('profiles').insert({
                'id': user.id,
                'name': username
            }).execute()

            sleep(2)

            if session:
                st.session_state['user'] = user
                st.rerun()

        # Error if passwords do not  match
        else:
            st.error('Passwords do not match!', icon='❌')
