import streamlit as st
from utils.auth import sign_out, init_connection

supabase = init_connection()

# Sidebar

with st.sidebar:
    # Log out 
    if st.button('Sign out'):
        sign_out_status = sign_out(supabase)
        st.write(sign_out)

        # Wipe out 'user' and 'user_id' after sucessful sign out
        if sign_out_status:
            st.session_state['user'] = None
            st.session_state['user_id'] = None
            st.rerun()

        else:
            st.error('Could not sign out. Please try again', icon='❌')

