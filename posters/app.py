import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_posters(movie_id):

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MTg4ZjllMmYyNDI2MDlkOGI1NzNhNTVkOWZlY2JjZSIsIm5iZiI6MTc1MDA2MDY2NS4wMzMsInN1YiI6IjY4NGZjZTc5YzAxMDE0YjQ3OTFlYzliZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.h0liwIO_yUrRsaox5i0R3dA9K5vnP5WnGHvuwB0vQAs"
    }
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError if rgiesponse wasn't 200
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get['poster_path']
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    #use enumerate to preserve the index and the extract top 5 similar movies
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]]['title']) #store the names in a list
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title("🎥 Suggestify 🍿")
st.subheader("Your Personal Movie Recommender")

selected_movie_name = st.selectbox('Choose a movie you like',movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])

