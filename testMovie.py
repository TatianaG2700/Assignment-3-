import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movie data
movies = pd.read_csv("movies.csv")

# AI Engine - TF-IDF and Cosine Similarity
# Combine features for better recommendations
movies["features"] = movies["genre"] + " " + movies["description"]
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["features"])
similarity = cosine_similarity(tfidf_matrix)

# Function to get recommendations
def get_recommendations(title, num=5):
    idx = movies[movies["title"] == title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[1:num+1]  # skip the movie itself
    recommended = [movies.iloc[i[0]] for i in scores]
    return recommended

# Streamlit UI
st.title("🎬 AI Movie Recommendation System")
st.write("Select a movie you like and get AI-powered recommendations!")

selected_movie = st.selectbox("Choose a movie:", movies["title"])

if st.button("Get Recommendations"):
    st.subheader(f"Because you liked {selected_movie}:")
    results = get_recommendations(selected_movie)
    for movie in results:
        st.write(f"🎬 **{movie['title']}** ({movie['year']})")
        st.write(f"Genre: {movie['genre']} | ⭐ Rating: {movie['rating']}")
        st.write(f"_{movie['description']}_")
        st.write("---")
