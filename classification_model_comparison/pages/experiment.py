import streamlit as st
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif

# Set page config:
# The title is "Experiment"
# Choose an icon for the page
# The layout is centered
# The sidebar is set to "auto"

st.set_page_config(
    'Experiment',
    '🧪',
    layout='centered',
    initial_sidebar_state='auto'
)

# Write a function to load the wine dataset from sklearn
# Should you cache it? Yes!
@st.cache_data()
def load_wine_data():
    """
    Load wine dataset into a dataframe.
    """
    wine = load_wine()
    
    df = pd.DataFrame(wine.data, columns=wine.feature_names)
    df['target'] = wine.target
    
    return df


# Run the function to load the data
df = load_wine_data()

# Write a function for train/test split.
# Use stratification, and keep 30% of the data for the test set
# Should you cache it? Yes!
@st.cache_data()
def split_data():
    """
    Split dataset into train-test split (70/30 ratio).
    Split by maintaining the class distribution (stratify sampling).
    """
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, 
                                                        random_state=42, stratify=y)
    
    return X_train, X_test, y_train, y_test

# Run your train/test split function
X_train, X_test, y_train, y_test = split_data()

# Write a function to select features using SelectKbest and mutual_info_classif
# Should you cache it? Yes!
@st.cache_data()
def select_features(k):
    """
    Uses K best features using mutual information based feature selection.
    Returns a list of top K best feature names.
    """
    
    selector = SelectKBest(score_func=mutual_info_classif, k=k)
    
    # Fit and transform the data
    selector.fit_transform(X_train, y_train)
    # Get the boolean mask of selected features
    selected_mask = selector.get_support()
    
    # Extract the final feature names
    final_features = X_train.columns[selected_mask].tolist()
    
    return final_features


# Write a function that fits the selected model and computes the F1-score
# The function must return the F1-Score
# Inside this function, you must run feature selection
# Should you cache it? Yes!
@st.cache_data()
def fit_and_score(model_name, k):
    """
    Train the selected model using top K features.
    Computes F1-Score.
    Returns F1-Score.
    """
    
    # Run the feature selection
    feature_list = select_features(k)
    
    if model_name == 'Baseline':
        model = DummyClassifier(strategy='most_frequent', random_state=42)
        model.fit(X_train[feature_list], y_train)

    elif model_name == 'Decision Tree':
        model = DecisionTreeClassifier(criterion='gini', random_state=42)
        model.fit(X_train[feature_list], y_train)
   
    elif model_name == 'Random Forest':
        model = RandomForestClassifier(n_estimators=100, criterion='gini', random_state=42)
        model.fit(X_train[feature_list], y_train)
    
    else: 
        model =GradientBoostingClassifier(n_estimators=100, random_state=42)
        model.fit(X_train[feature_list], y_train)

    # Test and calculate score
    pred = model.predict(X_test[feature_list])    
    f1 = f1_score(y_test, pred, average='weighted')
    
    return f1


# Write a callback function that runs the model fitting and scoring function
# The callback appends the model, number of features, and score to the state.
# The callback takes 2 arguments: the model and the number of features to keep
@st.cache_data()
def train_test_model(model_name, k):
    """
    Calls fit_and_score function that returns the f1 score for the selected model.
    """
    
    f1_score = fit_and_score(model_name, k)
    
    # Append data to session state
    st.session_state['model'].append(model_name)
    st.session_state['num_features'].append(k)
    st.session_state['score'].append(f1_score)
    

if __name__ == "__main__":
    
    with st.container():
        st.title("🧪 Experiments")

    col1, col2 = st.columns(2)

    with col1:
        model = st.selectbox("Choose a model", ["Baseline", "Decision Tree", "Random Forest", "Gradient Boosted Classifier"])
    with col2:
        k = st.number_input("Choose the number of features to keep", 1, 13)

    # Plug in your callback and define the arguments
    st.button("Train", type="primary", on_click=train_test_model, args=(model, k))

    # Display the full dataset inside an expander

    if len(st.session_state['score']) != 0:
        st.subheader(f"The model has an F1-Score of: {st.session_state['score'][-1]}")
        