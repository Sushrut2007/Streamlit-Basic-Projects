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


@st.cache_data
def plot_content_over_time(yearly_count):
    """
    Create a line chart of year and total titles in each year.

    Args:
        yearly_count (Series): Time series containing index as year and yearly count.

    Returns:
        fig: Plotly line chart figure
    """
    
    fig = px.line(data_frame=yearly_count, x = yearly_count.index, y = yearly_count,
                  title="Title Added Overtime", labels={'x': 'Year', 'y': 'Total Titles Added'})

    return fig

@st.cache_data
def plot_type_ratio(title_ratio):
    """
    Create a pie chart for Movie vs TV Show ratio

    Args:
        title_ratio (Series): Series containing type and %

    Returns:
        fig: Plotly pie chart figure
    """

    fig = px.pie(names=title_ratio.index, values=title_ratio.values,
                 title="Movie VS TV Show Ratio")
   
    return fig


@st.cache_data
def plot_top_genre(df):
    """
    Create a bar chart for top genres.

    Args:
        df (DataFrame): Filtered DF

    Returns:
        fig: Plotly bar chart figure
    """ 

    # Extract the genre columns (dummy encoded), and sum the values for each
    genre_cols = df.columns[8:]
    top_genres = df[genre_cols].sum().sort_values(ascending=False).head(5)
    
    fig = px.bar(x=top_genres, y=top_genres.index, title='Top Genres',
                 labels={'x': 'Total Titles', 'y': 'Genre'})
   
    return fig


@st.cache_data
def plot_top_rating(df):
    """
    Create a bar chart for top ratings.

    Args:
        df (DataFrame): Filtered DF

    Returns:
        fig: Plotly bar chart figure
    """ 

   # Aggregate rating ratio using %

    rating_per = df['rating'].value_counts(normalize = True) * 100
    
    fig = px.bar(x=rating_per, y=rating_per.index, title='Top Ratings',
                 labels={'x': 'Total Titles (%) ', 'y': 'Rating'})
   
    return fig


@st.cache_data
def plot_by_country(country_count):
    """
    Create a scatter plot for countries having most titles.

    Args:
        country_count (DataFrame): DF having country name and title count

    Returns:
        fig: Plotly scatter plot figure
    """ 

    top_countries = country_count.head(10)

    fig = px.scatter(
        top_countries,
        x='country',
        y='count',
        size='count',
        color='count',
        hover_name='country',
        color_continuous_scale='Reds',
        size_max=60,
        title="Titles By Country" 
    )
   
    return fig

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

    if filtered_df.empty:
        st.warning('No titles found with these filters! Please adjust your search!')
        st.stop()
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
        country_prc = f"{round((top_country_count / filtered_df.shape[0]) * 100, 1)} % of all titles"

        st.metric('Top country', value=top_country, width="stretch", delta = country_prc, delta_arrow="off")
    
    # -------------------------------------------
    
    # Visualization plots

    col1, col2 = st.columns([1.5, 1])

    with col1:
        # Line chart
        year_fig = plot_content_over_time(yearly_count)
        st.plotly_chart(year_fig) # Plot

        # Bar chart (top genre)
        genre_fig = plot_top_genre(filtered_df)
        st.plotly_chart(genre_fig) # Plot

    with col2:
        # Pie chart
        ratio_fig = plot_type_ratio(title_type_ratio)
        st.plotly_chart(ratio_fig) # Plot

        # Bar chart (top ratings)
        rating_fig = plot_top_rating(filtered_df)
        st.plotly_chart(rating_fig) # Plot

    # Scatter plot 
    country_fig = plot_by_country(country_count)
    st.plotly_chart(country_fig) # Plot


if __name__ == "__main__":
    main()

