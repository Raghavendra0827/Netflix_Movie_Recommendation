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
    </style>
"""

def main():
    # st.title("Netflix Movie Recommendation Engine")
    # user_id_input = st.number_input("Enter User ID:", value=2378011)
    # user_id = int(user_id_input)

    # Dropdown menu with the list of items
    usr_id = [1488844,
 822109,
 885013,
 30878,
 823519,
 893988,
 124105,
 1248029,
 1842128,
 2238063,
 1503895,
 2207774,
 2590061,
 2442,
 543865,
 1209119,
 804919,
 1086807,
 1711859,
 372233,
 1080361,
 1245640,
 558634,
 2165002,
 1181550,
 1227322,
 427928,
 814701,
 808731,
 662870,
 337541,
 786312,
 1133214,
 1537427,
 1209954,
 2381599,
 525356,
 1910569,
 2263586,
 2421815,
 1009622,
 1481961,
 401047,
 2179073,
 1434636,
 93986,
 1308744,
 2647871,
 1905581,
 2508819,
 1578279,
 1159695,
 2588432,
 2423091,
 470232,
 2148699,
 1342007,
 466135,
 2472440,
 1283744,
 1927580,
 716874,
 4326,
 1546549,
 1493697,
 880166,
 535396,
 494609,
 1961619,
 883478,
 793564,
 1567202,
 573537,
 1972040,
 1838912,
 411705,
 2244518,
 584542,
 667730,
 2488120,
 1926776,
 38052,
 1196100,
 314933,
 1792741,
 769643,
 2477242,
 1421006,
 729846,
 1719610,
 1696031,
 1817215,
 406057,
 636262,
 1245406,
 1834590,
 593225,
 1011918,
 1665054,
 2630337]
    selected_item = st.selectbox("Select an item:", usr_id, default="822109")

    if st.button("Recommend Movies"):
        Recommend(selected_item, Movies)


def Recommend(User_ID, Movies):
    try:
        Movies['Estimate_Score'] = Movies['Movie_Id'].apply(lambda x: loaded_svd_model.predict(User_ID, x).est)
        Movie = Movies.sort_values('Estimate_Score', ascending=False)
    except:
        st.warning("Invalid User ID")

    st.header("Top 10 Recommended Movies:")
    for idx, movie_name in enumerate(Movie['Name'][:10]):
        st.write(f"{idx + 1}. {movie_name}")

    fig, ax = plt.subplots(figsize=(10, 6))
    heatmap_data = pd.DataFrame({'Names': Movie['Name'][:10], 'Priority': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]})
    heatmap_data['Priority'] = pd.to_numeric(heatmap_data['Priority'], errors='coerce').fillna(0)
    heatmap_data.set_index('Names', inplace=True)
    sns.heatmap(heatmap_data[['Priority']], annot=True, fmt="g", cmap="YlGnBu", cbar_kws={'label': 'Estimate Score'}, ax=ax)
    st.pyplot(fig)

if __name__ == "__main__":
    st.markdown(html_code, unsafe_allow_html=True)
    main()
