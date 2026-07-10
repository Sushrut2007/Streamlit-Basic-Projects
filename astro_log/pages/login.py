import streamlit as st
from utils.auth import init_connection, sign_in
from time import sleep

# Initiate database connection
supabase = init_connection()

st.title("Log In 🔐")

# Log in form
with st.form('login_form'):
    email = st.text_input('Email')
    password = st.text_input('Password ', type='password')

    if st.form_submit_button('Log in'):
        user, session = sign_in(supabase, email, password)

        if user and session:

            st.session_state['user_id'] = session.user.id
            st.session_state['user'] = user
            st.success('Sign in successful!', icon='✅')
            st.markdown('Redirecting to the dashboard..')
            sleep(2)

            st.rerun()
        else:
            st.error('Invalid email or password', icon='❌')

