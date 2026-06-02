import streamlit as st
import pandas as pd

# Set page config:
# The title is "Homepage"
# Choose an icon for the page
# The layout is centered
# The sidebar is set to "auto"

st.set_page_config(
    'Homepage',
    '🛖',
    layout='centered',
    initial_sidebar_state='auto'
)

# Initialize the state with the keys: [model, num_features, score]
# This is where we store the info to display the ranking
for key in ['model', 'num_features', 'score']:
    if key not in st.session_state:
        st.session_state[key] = []

# Write a function to display a DataFrame ranked in descending order of F1-Score
# The DataFrame has 3 columns: Model, Number of Features, F1-Score

def display_dataframe():
    # Create a dictionary from the relevant session state keys
    data = {
        'Model': st.session_state.get('model', []),
        'Number of Features': st.session_state.get('num_features', []),
        'F1-Score': st.session_state.get('score', [])
    }
    
    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":
    st.title("🏆 Model ranking")

    if len(st.session_state['model']) == 0:
        st.subheader("Train a model in the next page to see the results 👉")
    else:
        pass
        #Function that display the DataFrame runs here
        df = display_dataframe()
        
        st.write(st.session_state)
    
        st.write(df)