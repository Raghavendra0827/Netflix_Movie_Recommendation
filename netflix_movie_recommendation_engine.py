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

background_image = 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bmV0ZmxpeHxlbnwwfHwwfHx8MA%3D%3D'
html_code = f"""
    <style>
        body {{
            background-image: url('{background_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;  /* Set the height of the background to fill the viewport */
            margin: 0;  /* Remove default body margin */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .stApp {{
            background: none;  /* Remove Streamlit app background */
        }}
    </style>
"""

def main():
    st.title("Netflix Movie Recommendation Engine")
    # User input for User ID
    user_id_input = st.number_input("Enter User ID:", value=2378011)
    user_id = int(user_id_input)
    # Button to execute the recommendation function
    if st.button("Recommend Movies"):
        Recommend(user_id, Movies)

def Recommend(User_ID, Movies):
    try:
        Movies['Estimate_Score'] = Movies['Movie_Id'].apply(lambda x: loaded_svd_model.predict(User_ID, x).est)
        Movie = Movies.sort_values('Estimate_Score', ascending=False)
    except:
        st.warning("Invalid User ID")

    st.header("Top 10 Recommended Movies:")
    for idx, movie_name in enumerate(Movie['Name'][:10]):
        st.write(f"{idx + 1}. {movie_name}")

    # Create a heatmap of estimated scores
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Ensure the "Priority" column is numeric and has no missing values
    heatmap_data = pd.DataFrame({'Names': Movie['Name'][:10], 'Priority': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]})
    heatmap_data['Priority'] = pd.to_numeric(heatmap_data['Priority'], errors='coerce').fillna(0)
    heatmap_data.set_index('Names', inplace=True)
    sns.heatmap(heatmap_data[['Priority']] annot=True, fmt="g", cmap="YlGnBu", cbar_kws={'label': 'Estimate Score'}, ax=ax)
    
    # Display the heatmap using Streamlit's st.pyplot()
    st.pyplot(fig)

if __name__ == "__main__":
    st.markdown(html_code, unsafe_allow_html=True)
    main()
