import pickle
import streamlit as st
import requests
import pandas as pd

# ---------- Helper Functions ----------

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        data = response.json()

        if 'poster_path' not in data or data['poster_path'] is None:
            return "https://via.placeholder.com/300x450?text=No+Image"

        full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return full_path
    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/300x450?text=Error"

def recommend(movie, num):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:num + 1]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# ---------- Streamlit UI Setup ----------

st.set_page_config(page_title="Movie Recommender 🎬", page_icon="🎥", layout="wide")

# ---------- Custom CSS ----------

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #FF6347;
            font-size: 48px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #555;
            margin-bottom: 30px;
        }
        .card {
            border-radius: 10px;
            background-color: #f9f9f9;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        .card:hover {
            transform: scale(1.05);
        }
        .movie-title {
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------

st.markdown("<div class='main-title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find your next favorite movie based on what you love 🍿</div>", unsafe_allow_html=True)
st.markdown("<hr/>", unsafe_allow_html=True)

# ---------- Load Data ----------
movies = pd.read_csv('movies.csv')
similarity = pickle.load(open('cosine_similarity.pkl', 'rb'))

# ---------- User Inputs ----------
movie_list = movies['title'].values
selected_movie = st.selectbox("🎞️ Select a movie you like", movie_list)

num = st.slider("📊 Number of recommendations to show", min_value=1, max_value=20, value=5, step=1)

# ---------- Recommend Button ----------
if st.button('🎯 Show Recommendations'):
    with st.spinner("🔍 Fetching recommendations... please wait..."):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, num)

    st.markdown(f"<h3 style='color:#6c63ff;'>✨ Top {num} Movies You Might Enjoy:</h3>", unsafe_allow_html=True)

    cols = st.columns(5)  # Create fixed columns
    for i in range(num):
        with cols[i % 5]:  # Place 5 per row
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{recommended_movie_names[i]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
