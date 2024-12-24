import streamlit as slt
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    api_key = "ae53aa33b6fd96a078107b1f0d772550"
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")
    data = response.json()
    if "poster_path" in data and data["poster_path"] is not None:
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# Recommend movies based on similarity matrix
def recommend(movie):
    recommended_movies = []
    recommended_posters = []

    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similar[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))
    except IndexError:
        slt.error("Movie not found in database.")
    return recommended_movies, recommended_posters

# Load saved movie data and similarity matrix
movie_dict = pickle.load(open("movie_dic.pkl", "rb"))
movies = pd.DataFrame(movie_dict)
similar = pickle.load(open("similar.pkl", "rb"))

# Streamlit interface
slt.title("SSR Movie Recommendation System Project🎬🎬🎬")
select_movie_name = slt.selectbox("Enter the name of a movie:", movies["title"].values)

if slt.button("RECOMMEND"):
    names, posters = recommend(select_movie_name)

    if names:
        col1, col2, col3, col4, col5 = slt.columns(5)

        with col1:
            slt.text(names[0])
            slt.image(posters[0])
        with col2:
            slt.text(names[1])
            slt.image(posters[1])
        with col3:
            slt.text(names[2])
            slt.image(posters[2])
        with col4:
            slt.text(names[3])
            slt.image(posters[3])
        with col5:
            slt.text(names[4])
            slt.image(posters[4])
    else:
        slt.error("No recommendations found.")
