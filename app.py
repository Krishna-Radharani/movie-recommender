import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os
import gdown
import pickle

url = "https://drive.google.com/uc?export=download&id=1s5vnCT_K9-OeqlOJVn__WqA-v6rZ1WaE"
output = "similarity.pkl"

# Download if not already present
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Load the pickle file
with open(output, 'rb') as f:
    similarity = pickle.load(f)

# Optional: confirm
print("similarity.pkl loaded successfully!")


# Cache posters to avoid repeated requests
poster_cache = {}

def fetch_poster(movie_id):
    if movie_id in poster_cache:
        return poster_cache[movie_id]

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d3a9fb9fae936a69b9ce858039917045&language=en-US"
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            poster_url = "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"[ERROR] Poster fetch failed for ID {movie_id}: {e}")
        poster_url = "https://via.placeholder.com/500x750?text=No+Image"

    poster_cache[movie_id] = poster_url
    return poster_url


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.2)  # delay to avoid rate-limiting

    return recommended_titles, recommended_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Pick a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"**{names[i]}**")
            st.image(posters[i], use_container_width=True)  # ✅ fixed
