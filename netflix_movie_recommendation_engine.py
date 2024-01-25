import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import matplotlib.pyplot as plt

Movies = pd.read_csv('/content/Movies.csv')
Movies.drop(columns = ["Unnamed: 0"], inplace = True)

with open('svd_model.pkl', 'rb') as file:
    loaded_svd_model = pickle.load(file)

def Recommend(User_ID, Movies):
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

if __name__ == "__main__":
    user_id_input = st.text_input("Enter User ID:", 1488844)
    user_id = int(user_id_input)
    try:
      Recommend(user_id, Movies)
    except:
      st.warning("Invalid User ID")



