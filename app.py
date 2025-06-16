import pandas as pd
import streamlit as st
import pickle
import os
import base64
import gdown

def download_similarity():
    url = 'https://drive.google.com/uc?id=1MCvxJ6ksRHBz-MFI1eclIzQRED1sM_iM'
    output = 'similarity.pkl'
    gdown.download(url, output, quiet=False)

download_similarity()


def fetch_local_poster(movie_title):
    safe_title = "".join(c for c in movie_title if c.isalnum() or c in (" ", "_")).rstrip()
    file_path = f"posters/{safe_title}.jpg"
    if os.path.exists(file_path):
        return file_path
    else:
        return "posters/placeholder.jpeg"  # use a local placeholder image

# --- Recommend logic ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_local_poster(title))

    return recommended_movies, recommended_posters

@st.cache_resource
def load_data():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return pd.DataFrame(movies_dict), similarity

movies, similarity = load_data()


# --- Streamlit UI ---
st.markdown("<h1 style='text-align: center;'>🎥 Suggestify 🍿</h1>", unsafe_allow_html=True)
st.subheader("Your Personal Movie Recommender")

selected_movie_name = st.selectbox('Choose a movie you like', movies['title'].values)

# --- Image encoding helper ---
def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], caption=names[idx], use_container_width=True)
