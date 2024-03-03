#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import random
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import streamlit as st
# Set the background color
#st.set_page_config(layout="wide", page_title="Movie Recommendation App", page_icon=":clapper:", theme="light", background_color="#e6f1f7")

warnings.filterwarnings("ignore")
background_image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOku1la2asHxadGeG8mnFJ-7WUnc-T4YlW_A&usqp=CAU'
html_code = f"""
    <style>
        body {{
            background-image: url('{background_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .stApp {{
            background: none;
        }}
        .title {{
            color: white;
        }}
        .movie-title {{
            color: orange;
        }}
    </style>
"""

st.markdown(html_code, unsafe_allow_html=True)

def initial_description():
    st.title("Movie Recommendation App")
    st.write("Welcome to the Movie Recommendation App!")
    st.write("Enter a movie ID below to get recommendations based on its genre.")
    #st.write("Imported CSV:")
    st.write(pd.read_csv(r"APP_2/train_data.txt", sep=":::", header=None, names=["ID", "Title", "Genre", "Description"]))

# Read the data
try:
    columns = ["ID", "Title", "Genre", "Description"]
    data = pd.read_csv(r"APP_2/train_data.txt", sep=":::", header=None, names=columns)
except Exception as e:
    st.error(f"Error reading the data: {e}")

# Clean the data
for col in ["Title", "Genre", "Description"]:
    data[col] = data[col].str.lower().str.strip()

# Recommendation functions
def recommend(ID):
    try:
        Genre = data[data.ID == ID]["Genre"]
        til = list(data[data.ID == ID]["Title"])[0]
        till = extract_ge(til)
        Movies = data[data.Genre == "drama"]["Title"].to_frame()
        lst = Movies.Title.to_list()
        return extract_genres(lst, ID, till, til)
    except Exception as e:
        st.error(f"Error recommending movies: {e}")

def extract_ge(sentence):
    ge = []
    words = word_tokenize(sentence)
    for word in words:
        if wordnet.synsets(word, pos=wordnet.NOUN):
            if not word.isdigit():
                ge.append(word.capitalize())
            else:
                ge.append(word)        
    return ge

def extract_genres(lst, ID, till, til):
    global Moviee_Title, genres
    genres = []
    Moviee_Title = []
    
    for ttl in lst:
        words = word_tokenize(ttl)
        for word in words:
            if wordnet.synsets(word, pos=wordnet.NOUN):
                if not word.isdigit():
                    genres.append(word.capitalize())
                else:
                    genres.append(word)
        if len(set(genres).intersection(set(till))) >= 1:
            Moviee_Title.append(ttl)
            genres = []
        else:
            genres = []
    
    if til in Moviee_Title:
        del Moviee_Title[Moviee_Title.index(til)]
    
    num = 10 - len(Moviee_Title)
    if num < 0:
        Moviee_Title = Moviee_Title[:10]
    else:
        for _ in range(0, num):
            Moviee_Title.append(random.choice(lst))
    
    return Moviee_Title,til

# Streamlit app
def main():
    # Take input ID from the user
        # Set background image using container
  
    try:
        ID = st.number_input("Enter Movie ID:", value=1)
    except Exception as e:
        st.error(f"Error getting user input: {e}")
    
    # Add a submit button for ID input
    submitted = st.button("Submit")
    
    # Call the recommend function with the given ID on submit
    if submitted:
        try:
            movie_titles,t = recommend(ID)
        except Exception as e:
            st.error(f"Error getting movie recommendations: {e}")
        
        # Display the recommended movies and image in rows
        st.title("Currently Watching Movie")
        st.header(t.title())

# Displaying the image
        image_url = "https://i.pinimg.com/originals/6a/a5/e9/6aa5e969821d426d3d828fd08921c73b.png"
        st.image(image_url, caption=t.title(), use_column_width=True)
        st.title("Recommended Movies:")
        st.write("Enjoy discovering new movies!")
        num_columns = 5  # Number of columns for displaying movies
        
        # Calculate the number of rows needed
        num_rows = len(movie_titles) // num_columns
        if len(movie_titles) % num_columns != 0:
            num_rows += 1
        
        # Display movies and image in rows
        for i in range(num_rows):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                idx = i * num_columns + j
                if idx < len(movie_titles):
                    try:
                        cols[j].write(movie_titles[idx].title(), unsafe_allow_html=True)
                        cols[j].image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSePkMigckVrgjrtsMpymhsmB0oc_i408ge-A&usqp=CAU", caption="Recommended Movie", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error displaying movie info: {e}")

if __name__ == "__main__":
    initial_description()
    main()
