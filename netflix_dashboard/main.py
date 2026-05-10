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


@st.cache_data()
def filter_data(df, content_type, rating_type, countries, year_range):
    """
    Filter entire dataset by content type,
    rating, country and release year range.

    Args:
        df (DataFrame): Complete dataset

    Returns:
        filtered_df: filtered DF
    """
    filtered_df = df.copy()

    # Filter by content
    if content_type != 'All':
        filtered_df = filtered_df[filtered_df['type'] == content_type]

    # Filter by rating 
    if rating_type != 'All':
        filtered_df = filtered_df[filtered_df['rating'] == rating_type]

    # Filter by year range
    filtered_df = filtered_df[(filtered_df['release_year'] >= year_range[0]) &
                              (filtered_df['release_year'] <= year_range[1])]

    # Filter by country
    if countries: # Check if atleast 1 is selected
            pattern = '|'.join(countries)
            filtered_df = filtered_df[filtered_df['country'].str.contains(pattern)]

    return filtered_df

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
        type_options = ['All'] + list(df['type'].unique())
        content_type = st.selectbox('Content type', options=type_options)

        # Select rating ()
        rating_options = ['All'] + list(df['rating'].unique())
        rating_type = st.selectbox('Rating', options=rating_options)

        # Select country
        country_names = get_country_count(df) # Call function
        unique_names = country_names['country'].unique()

        countries = st.multiselect('Country', options=unique_names, default=country_names.loc[0, 'country'])

        # Select release year range
        min_year = df['release_year'].min()
        max_year = df['release_year'].max()

        year_range = st.slider('Release year range', min_value=min_year, max_value=max_year, value=(min_year, max_year))

        # Extra output
        st.divider()
        st.write(f'Showing {df.shape[0]} titles')  
    # -------------------------------------------

    # Filter dataset
    filtered_df = filter_data(df, content_type, rating_type, countries, year_range)
    # -------------------------------------------

    # Aggregate data (used for both KPIs and Charts)
    title_type_ratio = get_type_ratio(filtered_df) # Type ratio
    yearly_count = get_yearly_count(filtered_df) # Yearly count
    country_count = get_country_count(filtered_df) # Country count
    # -------------------------------------------
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.3])
    
    with col1:
        if content_type == 'All':
            delta_text = "Movies + TV Shows"
        elif content_type == 'Movie':
            delta_text = "Movies"
        else:
            delta_text = "TV Shows"
        st.metric('Total titles', value=filtered_df.shape[0], delta=delta_text, delta_arrow="off")
    
    with col2:
        # Extract the movie and show %
        movie_number = title_type_ratio.get('Movie', 0)
        tv_number = title_type_ratio.get('TV Show', 0)

        movie_prc = f"{movie_number:.1f}%"
        show_prc = f"{tv_number:.1f}% TV Shows"

        st.metric('Movies', value=movie_prc, delta=show_prc, delta_color="violet", delta_arrow="off")

    with col3:
        # Extract the peak year and title count
        peak_year = yearly_count.idxmax()
        peak_count = f"{yearly_count.max()} titles added"

        st.metric('Peak year added', value=peak_year, delta=peak_count, delta_arrow="off")

    with col4:
        # Extract top country name and count
        top_country = country_count.iloc[0]['country']
        top_country_count = country_count.iloc[0]['count']
        country_prc = f"{(top_country_count / filtered_df.shape[0]) * 100} % titles added"

        st.metric('Top country', value=top_country, width="stretch", delta = country_prc, delta_arrow="off")
        
if __name__ == "__main__":
    main()

