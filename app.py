import streamlit as st
import pickle
import requests

# loading the trained model
movie_data = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list=movie_data['title'].values

# Add title on the page

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=b680f3c0b987629cbc55dac2602a8057&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movie_data[movie_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies:
        recommended_movies_posters.append(fetch_poster(movie_data.iloc[i[0]].movie_id))
        recommended_movies.append(movie_data.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters

st.title("Movie Recommender System")

st.write("""
# Simple Movie Recommender System
""")
st.write("This is a simple movie recommender system built with Streamlit and Python.")

st.write("""
### How does it work?
""")
st.write("The recommender system uses the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv) dataset to recommend movies to users based on their ratings.")

selected_movie = st.selectbox(
    'Select a movie',
     movie_list) 

if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


