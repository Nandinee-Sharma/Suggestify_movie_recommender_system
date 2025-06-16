import pandas as pd
import streamlit as st
import pickle
import os
import base64
import gdown
import zipfile

def download_similarity():
    url = 'https://drive.google.com/uc?id=1MCvxJ6ksRHBz-MFI1eclIzQRED1sM_iM'
    output = 'similarity.pkl'
    gdown.download(url, output, quiet=False)

# --- Download and extract posters.zip ---
def download_and_extract_posters():
    posters_dir = "posters"
    if not os.path.exists(posters_dir) or len(os.listdir(posters_dir)) == 0:
        os.makedirs(posters_dir, exist_ok=True)
        zip_path = "posters.zip"
        posters_zip_file_id = "1Aan285Ir0ZXtaeJVFaulZjemXJJ--8pW"
        gdown.download(f"https://drive.google.com/uc?id={posters_zip_file_id}", zip_path, quiet=False)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(posters_dir)
        os.remove(zip_path)


download_similarity()
download_and_extract_posters()

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


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], caption=names[idx], use_container_width=True)
