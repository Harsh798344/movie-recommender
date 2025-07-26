import requests
import streamlit as st
import  pickle
import pandas as pd

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US',
            timeout=5  # seconds
        )
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"



def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommeded_movies =[]
    recommeded_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommeded_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommeded_movies_posters.append(fetch_poster(movie_id))
    return recommeded_movies,recommeded_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System ')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)
if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])