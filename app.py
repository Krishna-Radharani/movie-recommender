import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os
import urllib.request

# ===== Download similarity.pkl from Hugging Face =====
SIMILARITY_FILE = "similarity.pkl"
HF_URL = "https://huggingface.co/datasets/Krishna-Radharani-123/movie-recommender-assets/resolve/main/similarity.pkl"

if not os.path.exists(SIMILARITY_FILE):
    urllib.request.urlretrieve(HF_URL, SIMILARITY_FILE)

# ===== Load data =====
with open('movie_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)

with open(SIMILARITY_FILE, 'rb') as f:
    similarity = pickle.load(f)

# ===== Poster Cache =====
poster_cache = {}


def fetch_poster(movie_id):
    if movie_id in poster_cache:
        return poster_cache[movie_id], ""

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d3a9fb9fae936a69b9ce858039917045&language=en-US"
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        overview = data.get("overview", "No description available.")
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        poster_url = "https://via.placeholder.com/500x750?text=No+Image"
        overview = "Description unavailable."

    poster_cache[movie_id] = (poster_url, overview)
    return poster_url, overview


# ===== Recommendation Logic =====
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_titles = []
        recommended_posters = []
        recommended_overviews = []

        for i in movie_list:
            movie_id = movies.iloc[i[0]].id
            recommended_titles.append(movies.iloc[i[0]].title)
            poster, overview = fetch_poster(movie_id)
            recommended_posters.append(poster)
            recommended_overviews.append(overview)
            time.sleep(0.2)  # Prevent rate limiting

        return recommended_titles, recommended_posters, recommended_overviews
    except Exception as e:
        st.error(f"Recommendation failed: {e}")
        return [], [], []

# ===== Streamlit UI =====
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
        .recommend-box {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 20px;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 12px;
            background: #f9f9f9;
            box-shadow: 0 2px 10px rgba(0,0,0,0.07);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .recommend-box:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        .movie-desc {
            font-size: 16px;
            line-height: 1.6;
            text-align: justify;
            color: #444;
        }
        .movie-title {
            font-size: 20px;
            font-weight: 600;
            margin: 5px 0;
            color: #d6336c;
        }
        hr.custom-line {
            border: 0;
            height: 1px;
            background: #ddd;
            margin: 30px 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B; font-size: 48px;'>🎬 Movie Recommender</h1>
    <hr class='custom-line'>
""", unsafe_allow_html=True)

# Centered input
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_name = st.selectbox(
        "Select a movie you like:",
        movies['title'].values,
        index=None,
        placeholder="Start typing to search..."
    )

    if selected_movie_name and st.button("🎯 Recommend"):
        names, posters, overviews = recommend(selected_movie_name)
        if names:
            st.markdown("## 🎥 Recommendations\n")

            for i in range(5):
                youtube_query = f"{names[i]} official trailer"
                youtube_search_url = f"https://www.youtube.com/results?search_query={youtube_query.replace(' ', '+')}"

                st.markdown(f"""
                <div class='recommend-box'>
                    <img src="{posters[i]}" width="150px" style="border-radius: 8px;" />
                    <div>
                        <div class='movie-title'>{names[i]}</div>
                        <div class='movie-desc'>{overviews[i]}</div>
                        <a href="{youtube_search_url}" target="_blank" style="display:inline-block;margin-top:10px;padding:6px 12px;background-color:#FF4B4B;color:white;border-radius:6px;text-decoration:none;">▶ Watch Trailer</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

