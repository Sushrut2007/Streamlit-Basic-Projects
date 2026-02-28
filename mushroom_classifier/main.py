import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.ensemble import GradientBoostingClassifier

URL = "data/mushrooms.csv"
# List of the best features to be used
COLS = ['class', 'odor', 'gill-size', 'gill-color', 'stalk-surface-above-ring',
       'stalk-surface-below-ring', 'stalk-color-above-ring',
       'stalk-color-below-ring', 'ring-type', 'spore-print-color']

# Function to read the data
@st.cache_data()
def read_data(file_path, cols):
    try:
        df = pd.read_csv(file_path)
        df = df[cols] # Select the subset
    except FileNotFoundError:
        st.error('CSV file not found!', icon='⚠️')

    return df

# Function to fit the LabelEncoder
@st.cache_resource()
def encode_label(df):
    le = LabelEncoder()
    le.fit(df['class'])

    return le

# Function to fit the OrdinalEncoder
@st.cache_resource()
def encode_categories(df):
    oe = OrdinalEncoder()

    X_cols = df.columns[1:] # Select the columns
    oe.fit(df[X_cols])

    return oe

# Function to encode data
@st.cache_data()
def encode_data(df, _X_encoder, _y_encoder):
    df['class'] = _y_encoder.transform(df['class'])

    X_cols = df[1:]
    df[cols] = _X_encoder.transform(df[cols])
    
    return df

# Function to train the model
@st.cache_resource()
def train_model(df):
    X = df.drop('class', axis=1)
    y = df['class']

    gbc = GradientBoostingClassifier(max_depth=5, random_state=42)
    gbc.fit(X, y) # Train the model on full dataset

    return gbc

# Function to make a prediction
@st.cache_data()
def train_model(gbc, input):
    prediction = gbc.predict(input) # Predict

    return prediction

if __name__ == "__main__":
    st.title("Mushroom classifier 🍄")
    
    # Read the data
    df = read_data(URL)
    
    st.subheader("Step 1: Select the values for prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        odor = st.selectbox('Odor', ('a - almond', 'l - anisel', 'c - creosote', 'y - fishy', 'f - foul', 'm - musty', 'n - none', 'p - pungent', 's - spicy'))
        stalk_surface_above_ring = st.selectbox('Stalk surface above ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        stalk_color_below_ring = st.selectbox('Stalk color below ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
    with col2:
        gill_size = st.selectbox('Gill size', ('b - broad', 'n - narrow'))
        stalk_surface_below_ring = st.selectbox('Stalk surface below ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        ring_type = st.selectbox('Ring type', ('e - evanescente', 'f - flaring', 'l - large', 'n - none', 'p - pendant', 's - sheathing', 'z - zone'))
    with col3:
        gill_color = st.selectbox('Gill color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'g - gray', 'r - green', 'o - orange', 'p - pink', 'u - purple', 'e - red', 'w - white', 'y - yellow'))
        stalk_color_above_ring = st.selectbox('Stalk color above ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
        spore_print_color = st.selectbox('Spore print color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'r - green', 'o - orange', 'u - purple', 'w - white', 'y - yellow'))

    st.subheader("Step 2: Ask the model for a prediction")

    pred_btn = st.button("Predict", type="primary")

    # If the button is clicked:
    # 1. Fit the LabelEncoder
    # 2. Fit the OrdinalEncoder
    # 3. Encode the data
    # 4. Train the model

    x_pred = [odor, 
                gill_size, 
                gill_color, 
                stalk_surface_above_ring, 
                stalk_surface_below_ring, 
                stalk_color_above_ring, 
                stalk_color_below_ring, 
                ring_type, 
                spore_print_color]
    
    # 5. Make a prediction
    # 6. Format the prediction to be a nice text
    # 7. Output it to the screen
    