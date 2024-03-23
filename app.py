import streamlit as st
import requests

import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
# TfidfVectorizer - This is used to convert text data into numerical values
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

movies_data =pd.read_csv('movies.csv')

# File path from which to load pickled similarity data
pickle_file_path = 'similarity.pkl'

# Unpickle the similarity data from the file
with open(pickle_file_path, 'rb') as f:
    similarity = pickle.load(f)

print("Similarity data loaded successfully.")


url = "https://imdb146.p.rapidapi.com/v1/find/"


headers = {
	"X-RapidAPI-Key": "c3d046ca4dmsh278a376fcb52f38p19229cjsn1c727078f7ac",
	"X-RapidAPI-Host": "imdb146.p.rapidapi.com"
}

st.title('Cinemate: Movie Recommender')

list_of_all_titles = movies_data['title'].tolist()

movie_name = st.selectbox(
    'Hey, I am curious, what is your favorite movie?',
    list_of_all_titles)

# st.write('You selected:', "")


# st.button("Reset", type="primary")
if st.button('Recommend'):



    # Displaying an h2 header
    st.header(movie_name)

    col1, col2 = st.columns(2)
    querystring = {"query":movie_name}
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    res = response.json()
    # Extracting details
    title_name = res['titleResults']['results'][0]['titleNameText']
    release_year = res['titleResults']['results'][0]['titleReleaseText']
    title_type = res['titleResults']['results'][0]['titleTypeText']
    poster_image_url = res['titleResults']['results'][0]['titlePosterImageModel']['url']
    caption = res['titleResults']['results'][0]['titlePosterImageModel']['caption']
    top_credits = res['titleResults']['results'][0]['topCredits']

    with col1:
        st.image(poster_image_url)

    with col2:
        st.markdown(f"Release Year: {release_year}")
        title_type_truncated = ' '.join(title_type.split()[:10])
        st.markdown(f"Title Type: {title_type_truncated}")
        st.markdown(f"Caption: {caption}")
        # Displaying "Top Credits" section
        st.subheader("Top Credits:")
        for credit in top_credits:
            st.markdown(f"- {credit}")

     
    st.subheader("Recommendations")


    col1, col2, col3 = st.columns(3)

    list_of_all_titles = movies_data['title'].tolist()

    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    close_match = find_close_match[0]

    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

    print('Movies suggested for you : \n')

    i = 0

    finalList = []

    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index==index]['title'].values[0]
        if (i<4):
            finalList.append(title_from_index)
            print(i, '.',title_from_index)
            i+=1



    with col1:
        querystring = {"query":finalList[1]}
        response = requests.get(url, headers=headers, params=querystring)
        # print(response.json())
        res = response.json()
        # Assuming res contains the JSON data
        print(res)

        # Get the URL of the poster for the first movie
        first_movie_poster_url = res['titleResults']['results'][0]['titlePosterImageModel']['url']
        # Assuming res contains the JSON data

        # Get the name of the first movie
        first_movie_name = res['titleResults']['results'][0]['titleNameText']

        st.markdown(f" {first_movie_name}")
        st.image(first_movie_poster_url)

    with col2:
        querystring = {"query":finalList[2]}
        response = requests.get(url, headers=headers, params=querystring)
        # print(response.json())
        res = response.json()
        # Assuming res contains the JSON data

        # Get the URL of the poster for the first movie
        first_movie_poster_url = res['titleResults']['results'][0]['titlePosterImageModel']['url']
        # Assuming res contains the JSON data

        # Get the name of the first movie
        first_movie_name = res['titleResults']['results'][0]['titleNameText']
        st.markdown(f" {first_movie_name}")
        st.image(first_movie_poster_url)

    with col3:
        querystring = {"query":finalList[3]}
        response = requests.get(url, headers=headers, params=querystring)
        # print(response.json())
        res = response.json()
        # Assuming res contains the JSON data

        # Get the URL of the poster for the first movie
        first_movie_poster_url = res['titleResults']['results'][0]['titlePosterImageModel']['url']
        # Assuming res contains the JSON data

        # Get the name of the first movie
        first_movie_name = res['titleResults']['results'][0]['titleNameText']
        st.markdown(f" {first_movie_name}")
        st.image(first_movie_poster_url)