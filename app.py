import streamlit as st
import pickle
import requests
import pandas as pd

def fetch_poster(movie_id):
    key = "7c14bd948861ebff043c86d89fbd75f4"
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US",
            timeout=65
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 MOVIE RECOMMENDER SYSTEM')

movie_list = movies['title'].values
selected_movie = st.selectbox('Choose a movie you like:', movie_list)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for j in range(5):
        with cols[j]:
            st.image(recommended_movie_posters[j])
            st.caption(recommended_movie_names[j])
