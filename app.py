import streamlit as st

st.set_page_config(layout="wide", page_title="Movie Recommender", page_icon="🎬")

import pickle
import pandas as pd
import requests
from urllib.parse import quote

st.markdown("""
<style>
img {
    border-radius: 15px;
    transition: transform .2s;
}
img:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

movies = pickle.load(open('movies.pkl','rb'))
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)
API_KEY = "e4395dc7875b76938047d5ebef4f61d6"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return None

    except requests.exceptions.RequestException:
        return None
    
def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_posters


st.markdown(
"""
<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>
<p style='text-align:center; font-size:18px; color:gray;'>
Developed by <b>Ahmad Khan</b>
</p>
""",
unsafe_allow_html=True
)
st.caption("Discover movies similar to your favorites 🎥")

selected_movie = st.selectbox(
    "Select Movie",
    movies['title'].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.write("Poster not available")

    with col2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1])
        else:
            st.write("Poster not available")

    with col3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2])
        else:
            st.write("Poster not available")

    with col4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3])
        else:
            st.write("Poster not available")

    with col5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4])
        else:
            st.write("Poster not available")