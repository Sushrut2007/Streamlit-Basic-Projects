import streamlit as st

# Initialize the session state

# Store the logged-in user in session state so all pages can share it and
# the app can switch between auth pages and the dashboard after signup/login.
if 'user' not in st.session_state:
    st.session_state['user'] = None


# Define all pages
signup_page = st.Page('pages/signup.py', title='Sign up')
login_page = st.Page('pages/login.py', title='Login in')
dashboard_page = st.Page('pages/dashboard.py', title='Dashboard', default=True)


# Dynamic navigation
if st.session_state['user'] is None:
    pg = st.navigation([signup_page, login_page])
else:
    pg = st.navigation([dashboard_page])

pg.run()