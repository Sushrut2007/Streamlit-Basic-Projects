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
@st.cache_data(show_spinner="Fetching_data...")
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
@st.cache_data(show_spinner="Encoding data...")
def encode_data(df, _X_encoder, _y_encoder):
    # CRITICAL: Copy the dataframe to avoid mutating the cached object in-place
    df_encoded = df.copy()
    df_encoded['class'] = _y_encoder.transform(df_encoded['class'])

    X_cols = df_encoded.columns[1:]
    df_encoded[X_cols] = _X_encoder.transform(df_encoded[X_cols])
    
    return df_encoded

# Function to train the model
@st.cache_resource(show_spinner="Training model....")
def train_model(df):
    X = df.drop('class', axis=1)
    y = df['class']

    gbc = GradientBoostingClassifier(max_depth=5, random_state=42)
    gbc.fit(X, y) # Train the model on full dataset

    return gbc

# Function to make a prediction
@st.cache_data(show_spinner="Making prediction....")
def make_prediction(_model, _X_encoder, X_pred):

    features = [each[0] for each in X_pred]
    features = np.array(features).reshape(1,-1)
    encoded_features = _X_encoder.transform(features)

    pred = _model.predict(encoded_features)
  
    return pred[0]

if __name__ == "__main__":
    st.title("Mushroom classifier 🍄")
    
    # Read the data
    df = read_data(URL, COLS)
    
    st.subheader("Step 1: Select the values for prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        odor = st.selectbox('Odor', ('a - almond', 'l - anisel', 'c - creosote', 'y - fishy', 'f - foul', 'm - musty', 'n - none', 'p - pungent', 's - spicy'))
        stalk_surface_above_ring = st.selectbox('Stalk surface above ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        stalk_color_below_ring = st.selectbox('Stalk color below ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
    with col2:
        gill_size = st.selectbox('Gill size', ('b - broad', 'n - narrow'))
        stalk_surface_below_ring = st.selectbox('Stalk surface below ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
        ring_type = st.selectbox('Ring type', ('e - evanescente', 'f - flaring', 'l - large', 'n - none', 'p - pendant'))
    with col3:
        gill_color = st.selectbox('Gill color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'g - gray', 'r - green', 'o - orange', 'p - pink', 'u - purple', 'e - red', 'w - white', 'y - yellow'))
        stalk_color_above_ring = st.selectbox('Stalk color above ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
        spore_print_color = st.selectbox('Spore print color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'r - green', 'o - orange', 'u - purple', 'w - white', 'y - yellow'))

    st.subheader("Step 2: Ask the model for a prediction")

    pred_btn = st.button("Predict", type="primary")

    # Prepare the model and encoders as soon as data is loaded (cached)
    # 1. Fit the LabelEncoder
    le = encode_label(df)
    # 2. Fit the OrdinalEncoder
    oe = encode_categories(df)
    # 3. Encode the data
    df_encoded = encode_data(df, oe, le)
    # 4. Train the model
    gbc = train_model(df_encoded)

    # If the button is clicked:
    if pred_btn:

        X_pred = [odor, 
                  gill_size, 
                  gill_color, 
                  stalk_surface_above_ring, 
                  stalk_surface_below_ring, 
                  stalk_color_above_ring, 
                  stalk_color_below_ring, 
                  ring_type, 
                  spore_print_color]
        
        # 5. Make a prediction
        pred = make_prediction(gbc, oe, X_pred)
        
        # 6. Format the prediction to be a nice text
        if pred==1:
            text_display = "The mushroom is poisonous 💀"
        else:
            text_display = "The mushroom is edible 🥄"
        # 7. Output it to the screen
        st.write(text_display)
    