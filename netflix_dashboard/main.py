import streamlit as st
import pandas as pd 
import plotly.express as px


@st.cache_data(show_spinner="Loading titles...")
def load_data(file_path):
    """
    Load cleaned netflix titles dataset.

    Args:
        file_path (string): Dataset path

    Returns:
        df: Cleaned dataframe
    """
    df = pd.read_csv(file_path)

    return df


@st.cache_data()
def get_type_ratio(df):
    """
    Calculate the ratio of Movie vs TV Shows.

    Args:
        df (DataFrame): Filtered DF

    Returns:
        ratio: Pandas series 
    """

   # Movie & TV Shows ratio (in %)
    ratio = df['type'].value_counts(normalize=True) * 100 # Get % for everything
    
    return ratio
   

@st.cache_data
def get_yearly_count(df):
    """
    Get count of titles added to Netflix in each year.

    Args:
        df (DataFrame):Filtered DF
    
    Returns:
        yearly_count: Series with yearly title count 
    """

    date_series = pd.to_datetime(df['date_added'].str.strip()) # Clean and convert to datetime
    yearly_count = date_series.dt.year.value_counts()
    yearly_count = yearly_count.sort_index() # 2008, 2009,... 2021

    return yearly_count



@st.cache_data
def get_country_count(df):
    """
    Get unique country names, and their 
    occurance in different titles.
    Useful because the country names in original df
    might have mixed country names in a single title.

    Args:
        df (DataFrame): Filtered DF

    Returns:
        DataFrame: DF containing country name and occurance
    """

    country_count = (df['country'].
                str.split(','). # 1. Split strings by comma and space
                explode(). # 2. Explode the lists into individual rows
                str.strip(). # 3. Clean the string to remove white space (if any)
                value_counts(). # 4. Then count the values!
                reset_index())  

    country_count.columns = ['country', 'count'] # Rename columns

    return country_count



def main():
    st.title('🎬 Netflix Content Dashboard')
    st.caption("Explore what's on Netflix — by genre, country, rating, and time")
    st.divider()
    # -------------------------------------------

    # Load dataset
    df = load_data('data/clean_netflix_titles.csv')
     # -------------------------------------------

    # Sidebar filters
    with st.sidebar:
        st.subheader('Filters')

        # Select title type (Movie / TV show )
        title_type = st.selectbox('Content type', options=df['type'].unique())

        # Select rating ()
        rating_type = st.selectbox('Rating', options=df['rating'].unique())

        # Select country
        country_names = get_country_count(df) # Call function
        unique_names = country_names['country'].unique()

        countries = st.multiselect('Country', options=unique_names, default=country_names.loc[0, 'country'])

        # Select release year range
        min_year = df['release_year'].min()
        max_year = df['release_year'].max()

        year_range = st.slider('Release year range', min_value=min_year, max_value=max_year)

        # Extra output
        st.divider()
        st.write(f'Showing {df.shape[0]} titles')  
    # -------------------------------------------

    # Aggregate data (used for both KPIs and Charts)
    title_type_ratio = get_type_ratio(df) # Type ratio
    yearly_count = get_yearly_count(df) # Yearly count
    country_count = get_country_count(df) # Country count
    # -------------------------------------------
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total titles', value=df.shape[0])


if __name__ == "__main__":
    main()

