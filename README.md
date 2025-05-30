# 🎬 Movie Recommender App

A stylish and intelligent movie recommender system built with **Streamlit**. Just pick a movie you like, and get 5 similar recommendations — complete with posters and descriptions!

> 🚀 **Live Demo**: [Click to Try It Out](https://movie-recommender-mndorgoirwxdjnt3xtwsvv.streamlit.app)

---

## ✨ Features

-  Search from thousands of movies
-  Get 5 intelligent movie recommendations
-  Includes posters & descriptions via TMDB
-  Hover animations and responsive layout
-  Runs instantly online via Streamlit Cloud

---

## 📦 Tech Stack

- `Streamlit` – For interactive UI
- `pandas`, `pickle` – For data processing
- `requests` – To fetch movie data from TMDB
- `Hugging Face Datasets` – To host `.pkl` files
- `TMDB API` – For movie posters & descriptions

---

## 📁 Dataset & Assets

- `movie_dict.pkl`: Metadata of movies
- `similarity.pkl`: Precomputed cosine similarity matrix  
  → Hosted here: [Hugging Face Repo](https://huggingface.co/datasets/Krishna-Radharani-123/movie-recommender-assets)

---

## 🚀 Run the App Locally

>  **Requires Python 3.7+**

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movie-recommender.git
cd movie-recommender
### 2. Install dependencies
```bash
pip install -r requirements.txt
### 3. Run the app
```bash
streamlit run app.py
### 4.Screenshot
![Screenshot 2025-05-30 141845](https://github.com/user-attachments/assets/b2bd7d16-4c7c-4600-99e4-69253cba5713)






