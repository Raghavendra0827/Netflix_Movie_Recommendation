import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import matplotlib.pyplot as plt

Movies = pd.read_csv('Movies.csv')
Movies.drop(columns=["Unnamed: 0"], inplace=True)

with open('svd_model.pkl', 'rb') as file:
    loaded_svd_model = pickle.load(file)

def Recommend(User_ID, Movies):
    try:
        Movies['Estimate_Score'] = Movies['Movie_Id'].apply(lambda x: loaded_svd_model.predict(User_ID, x).est)
        Movies = Movies.sort_values('Estimate_Score', ascending=False)

        st.header("Top 10 Recommended Movies:")
        for idx, movie_name in enumerate(Movies['Name'][:10]):
            st.write(f"{idx + 1}. {movie_name}")

        # Create a heatmap of estimated scores
        plt.figure(figsize=(10, 6))
        heatmap_data = Movies.pivot_table(index='User_ID', columns='Movie_Id', values='Estimate_Score')
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Estimate Score'})
        st.pyplot()
    except:
        st.warning("Invalid User ID")

if __name__ == "__main__":
    user_id_input = st.text_input("Enter User ID:")

    if user_id_input and user_id_input.isdigit():
        user_id = int(user_id_input)
        
        # Check if the entered User ID is in the list of Movie_Id
        if user_id in list(Movies['Movie_Id']):
            Recommend(user_id, Movies)
        else:
            st.warning("User ID not found in the dataset.")
    else:
        st.warning("Please enter a valid User ID.")
