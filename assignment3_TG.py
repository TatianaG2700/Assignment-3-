#Import of different features to store movies, to get the closest match during the search of the movies.
import json
import os
import random
from difflib import get_close_matches
from datetime import datetime

#Import streamlit for web-based UI
import streamlit as st
import pandas as pd

# ---------- PAGE CONFIGURATION ----------
#Set up the Streamlit page with title, icon, and layout
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS STYLING ----------
#Apply custom CSS — editorial cinema magazine aesthetic, warm and tactile
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Source+Sans+3:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --ink: white;
        --paper: black;
        --warm: #d4a574;
        --accent: black;
        --muted: #78716c;
        --divider: #e7e5e4;
        --card-bg: orange;
        --card-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
        --hover-shadow: 0 2px 8px rgba(0,0,0,0.1), 0 8px 24px rgba(0,0,0,0.06);
    }

    .stApp { background-color: var(--paper); }

    h1, h2, h3 { font-family: 'DM Serif Display', serif !important; color: var(--ink); }
    p, span, div, li, label { font-family: 'Source Sans 3', sans-serif; }

    /* --- Header --- */
    .brand {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem;
        color: var(--ink);
        letter-spacing: -0.5px;
        padding: 8px 0;
    }
    .brand-sub {
        font-family: 'Source Sans 3', sans-serif;
        font-size: 0.8rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 500;
    }

    /* --- Welcome --- */
    .welcome-strip {
        border-top: 3px solid var(--ink);
        border-bottom: 1px solid var(--divider);
        padding: 32px 0 28px 0;
        margin-bottom: 32px;
    }
    .welcome-strip h1 {
        font-size: 2.6rem;
        margin: 0;
        line-height: 1.15;
        color: var(--ink);
    }
    .welcome-strip .tagline {
        color: var(--muted);
        font-size: 1.05rem;
        margin-top: 6px;
        font-weight: 300;
    }
    .role-pill {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 3px 10px;
        border-radius: 3px;
        margin-top: 8px;
    }
    .role-admin {
        background: var(--accent);
        color: #fff1c1;
    }
    .role-user {
        background: var(--ink);
        color: #fff;
    }

    /* --- Movie Card --- */
    .film-card {
        background: var(--card-bg);
        border: 1px solid var(--divider);
        border-radius: 6px;
        padding: 24px 28px;
        margin: 16px 0;
        box-shadow: var(--card-shadow);
        transition: box-shadow 0.2s ease;
    }
    .film-card:hover { box-shadow: var(--hover-shadow); }
    .film-card .film-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.35rem;
        color: var(--ink);
        margin: 0 0 6px 0;
        line-height: 1.3;
    }
    .film-card .film-meta {
        font-size: 0.85rem;
        color: var(--muted);
        margin: 3px 0;
        font-weight: 400;
    }
    .film-card .film-meta strong { color: var(--ink); font-weight: 600; }
    .film-card .film-overview {
        color: #44403c;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-top: 12px;
        border-top: 1px solid var(--divider);
        padding-top: 12px;
    }
    .genre-chip {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--accent);
        border: 1px solid var(--accent);
        padding: 2px 8px;
        border-radius: 3px;
        margin: 2px 3px 2px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* --- Stat Block --- */
    .num-block {
        padding: 20px 0;
    }
    .num-block .big-num {
        font-family: 'DM Serif Display', serif;
        font-size: 2.4rem;
        color: var(--ink);
        line-height: 1;
    }
    .num-block .num-label {
        font-size: 0.78rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
        margin-top: 4px;
    }

    /* --- Section Dividers --- */
    .section-rule {
        border: none;
        border-top: 1px solid var(--divider);
        margin: 32px 0 24px 0;
    }
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 16px;
    }

    /* --- Small Cards --- */
    .pick-card {
        background: var(--card-bg);
        border: 1px solid var(--divider);
        border-radius: 6px;
        padding: 16px 18px;
        margin: 6px 0;
        box-shadow: var(--card-shadow);
    }
    .pick-card .pick-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1rem;
        color: var(--ink);
        margin: 0;
    }
    .pick-card .pick-detail {
        font-size: 0.8rem;
        color: var(--muted);
        margin-top: 4px;
    }
    .pick-card .pick-score {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--accent);
        font-weight: 500;
    }

    /* --- History Row --- */
    .log-row {
        border-left: 2px solid var(--warm);
        padding: 6px 0 6px 14px;
        margin: 6px 0;
    }
    .log-row .log-action {
        font-weight: 600;
        color: var(--ink);
        font-size: 0.88rem;
    }
    .log-row .log-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--muted);
    }

    /* --- Sidebar --- */
    div[data-testid="stSidebar"] {
        background: #fefdfb;
        border-right: 1px solid var(--divider);
    }
    div[data-testid="stSidebar"] .stButton button {
        text-align: left;
        font-family: 'Source Sans 3', sans-serif;
        font-weight: 500;
        border: none;
        background: transparent;
        color: var(--ink);
        padding: 8px 12px;
        border-radius: 4px;
        transition: background 0.15s;
    }
    div[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(0,0,0,0.04);
    }

    /* --- Login --- */
    .login-header {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        text-align: center;
        color: var(--ink);
        margin-bottom: 0;
    }
    .login-sub {
        text-align: center;
        font-size: 0.85rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 36px;
    }
</style>
""", unsafe_allow_html=True)


#User class
class User:
    #initialisation of the username and rated movies
    def __init__(self, username, role="user"):
        self.username = username
        self.rated_movies = {}
        self.watch_history = []  #stores timestamped watch/search history
        self.role = role  #role can be "user" or "admin"
#get name of user
    def getName(self):
        return self.username
#initialise of rate movie
    def rate_movie(self, title, rating):
        self.rated_movies[title] = rating
#get rated movies
    def get_rated_movies(self):
        return self.rated_movies
#Already rated movies
    def has_rated(self, title):
        return title in self.rated_movies
#Add a movie to the user's watch history with timestamp
    def add_to_history(self, title, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.watch_history.append({"title": title, "action": action, "time": timestamp})
#Get the full watch history
    def get_watch_history(self):
        return self.watch_history
#Check if the user is an admin
    def is_admin(self):
        return self.role == "admin"


#Movie class
class Movie:
    #initialisation
    def __init__(self, title, overview, popularity, poster_path, release_date, vote_average, vote_count):
        self.title = title
        self.overview = overview
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.genres = []
        self.user_ratings = []
#getters methods
    def get_title(self):
        return self.title

    def get_overview(self):
        return self.overview

    def get_popularity(self):
        return self.popularity

    def get_poster_path(self):
        return self.poster_path

    def get_release_date(self):
        return self.release_date

    def get_vote_average(self):
        return self.vote_average

    def get_vote_count(self):
        return self.vote_count

    def get_genres(self):
        return self.genres

    def get_user_rating_avg(self):
        if self.user_ratings:
            return round(sum(self.user_ratings) / len(self.user_ratings), 1)
        return None
#setters methods
    def set_title(self, title):
        self.title = title

    def set_overview(self, overview):
        self.overview = overview

    def set_popularity(self, popularity):
        self.popularity = popularity

    def set_poster_path(self, poster_path):
        self.poster_path = poster_path

    def set_release_date(self, release_date):
        self.release_date = release_date

    def set_vote_average(self, vote_average):
        self.vote_average = vote_average

    def set_vote_count(self, vote_count):
        self.vote_count = vote_count

    def setGenre(self, genre):
        self.genres.append(genre)

    def add_user_rating(self, rating):
        self.user_ratings.append(rating)


# ---------- DATA LOADING FUNCTIONS ----------

#Load genre data from JSON file and return a mapping of genre ID to name
@st.cache_data
def load_genres(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        genre_data = json.load(file)
    genre_map = {}
    for g in genre_data["genres"]:
        genre_map[g["id"]] = g["name"]
    return genre_map

#Load movie data from JSON file and return a list of Movie objects
def load_movies(filepath, genre_map):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    movies = []
    for item in data["results"]:
        movie = Movie(
            item.get("title"),
            item.get("overview"),
            item.get("popularity"),
            item.get("poster_path"),
            item.get("release_date"),
            item.get("vote_average"),
            item.get("vote_count")
        )
        for gid in item.get("genre_ids", []):
            if gid in genre_map:
                movie.setGenre(genre_map[gid])
        movies.append(movie)
    return movies


#Initialise session state variables for login, user data, and movies
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "movies_list" not in st.session_state:
    st.session_state.movies_list = []
if "genre_map" not in st.session_state:
    st.session_state.genre_map = {}
if "page" not in st.session_state:
    st.session_state.page = "home"

#predefined credentials of users with roles
if "usernames" not in st.session_state:
    st.session_state.usernames = ["admin"]
    st.session_state.passwords = ["admin123"]
    st.session_state.roles = ["admin"]




#Display a movie card with all details using editorial styling
def display_movie_card(movie):
    genres_html = " ".join([f'<span class="genre-chip">{g}</span>' for g in movie.get_genres()])
    st.markdown(f"""
    <div class="film-card">
        <div class="film-title">{movie.get_title()}</div>
        <div class="film-meta">{movie.get_release_date()} &middot; <strong>{movie.get_vote_average()}</strong>/10 &middot; {movie.get_vote_count()} votes &middot; popularity {movie.get_popularity()}</div>
        <div style="margin-top:8px;">{genres_html}</div>
        <div class="film-overview">{movie.get_overview()}</div>
    </div>
    """, unsafe_allow_html=True)

#Display a large number with a label underneath
def display_number(value, label):
    st.markdown(f"""
    <div class="num-block">
        <div class="big-num">{value}</div>
        <div class="num-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

#Display a section label in monospaced uppercase
def section_label(text):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

#Display a horizontal rule
def rule():
    st.markdown('<hr class="section-rule">', unsafe_allow_html=True)

#Search movie function that returns matching movies
def search_movies(query, movies_list):
    titles = [m.get_title() for m in movies_list]
    exact = [m for m in movies_list if query.lower() == m.get_title().lower()]
    if exact:
        return exact, "exact"
    partial = [m for m in movies_list if query.lower() in m.get_title().lower()]
    fuzzy_titles = get_close_matches(query, titles, n=5, cutoff=0.4)
    fuzzy = [m for m in movies_list if m.get_title() in fuzzy_titles]
    seen = set()
    results = []
    for m in partial + fuzzy:
        if m.get_title() not in seen:
            seen.add(m.get_title())
            results.append(m)
    return results, "suggestions"

#Similar recommendation of movie function
def get_recommendations(movie, movies_list):
    movie_genres = set(movie.get_genres())
    if not movie_genres:
        return []
    similar = []
    for m in movies_list:
        if m.get_title() != movie.get_title():
            shared = movie_genres.intersection(set(m.get_genres()))
            if shared:
                similar.append((m, len(shared)))
    similar.sort(key=lambda x: (x[1], x[0].get_vote_average()), reverse=True)
    return [m for m, _ in similar[:5]]

#Get personalised recommendations based on user's rated movies
def get_personalised_recommendations(user, movies_list):
    rated = user.get_rated_movies()
    if not rated:
        return []
    genre_scores = {}
    genre_counts = {}
    for title, rating in rated.items():
        for m in movies_list:
            if m.get_title() == title:
                for g in m.get_genres():
                    genre_scores[g] = genre_scores.get(g, 0) + rating
                    genre_counts[g] = genre_counts.get(g, 0) + 1
    genre_avg = {g: round(genre_scores[g] / genre_counts[g], 1) for g in genre_scores}
    recommendations = []
    for m in movies_list:
        if not user.has_rated(m.get_title()):
            score = sum(genre_avg.get(g, 0) for g in m.get_genres()) + m.get_vote_average()
            if score > 0:
                recommendations.append((m, round(score, 1)))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:10]
    

# ---------- PAGE FUNCTIONS ----------

# ===== LOGIN PAGE =====
#Displays the login and registration form
def login_page():
    st.markdown("")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-header">Movie Recommendation System</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">your film companion</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign in", "Create account"])

        with tab1:
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")

            if st.button("Sign in", use_container_width=True, type="primary"):
                for i in range(len(st.session_state.usernames)):
                    if login_user == st.session_state.usernames[i] and login_pass == st.session_state.passwords[i]:
                        user = User(login_user, st.session_state.roles[i])
                        st.session_state.current_user = user
                        st.session_state.logged_in = True
                        st.session_state.genre_map = load_genres("genre.json")
                        st.session_state.movies_list = load_movies("movie.json", st.session_state.genre_map)
                        st.session_state.page = "home"
                        st.rerun()
                st.error("Those credentials don't match. Give it another go.")

            st.markdown("---")
            st.caption("Try with `admin` / `admin123` for the full experience.")

        with tab2:
            reg_user = st.text_input("Pick a username", key="reg_user")
            reg_pass = st.text_input("Pick a password", type="password", key="reg_pass")

            if st.button("Create account", use_container_width=True, type="primary"):
                if reg_user in st.session_state.usernames:
                    st.error("That username's taken. Try another one or sign in.")
                elif reg_user and reg_pass:
                    st.session_state.usernames.append(reg_user)
                    st.session_state.passwords.append(reg_pass)
                    st.session_state.roles.append("user")
                    st.success(f"You're all set, {reg_user}. Head over to Sign in.")
                else:
                    st.warning("Need both a username and password.")


# ===== HOME / WELCOME PAGE =====
#Displays the welcome page with quick stats and navigation
def home_page():
    user = st.session_state.current_user
    movies = st.session_state.movies_list

    role_class = "role-admin" if user.is_admin() else "role-user"
    role_text = "admin" if user.is_admin() else "member"

    st.markdown(f"""
    <div class="welcome-strip">
        <h1>Good to see you, {user.getName()}.</h1>
        <div class="tagline">Here's what's happening in your collection today.</div>
        <span class="role-pill {role_class}">{role_text}</span>
    </div>
    """, unsafe_allow_html=True)

    # Quick numbers
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_number(len(movies), "films in collection")
    with col2:
        avg = round(sum(m.get_vote_average() for m in movies) / len(movies), 1)
        display_number(avg, "average rating")
    with col3:
        display_number(len(user.get_rated_movies()), "your ratings")
    with col4:
        display_number(len(user.get_watch_history()), "actions taken")

    rule()

    # Trending
    section_label("trending right now")
    trending = sorted(movies, key=lambda m: m.get_popularity(), reverse=True)[:5]
    cols = st.columns(5)
    for i, m in enumerate(trending):
        with cols[i]:
            st.markdown(f"""
            <div class="pick-card">
                <div class="pick-title">{m.get_title()[:22]}</div>
                <div class="pick-score">{m.get_vote_average()}/10</div>
                <div class="pick-detail">Pop. {m.get_popularity():.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    rule()

    # Highest rated
    section_label("highest rated")
    top = sorted(movies, key=lambda m: m.get_vote_average(), reverse=True)[:5]
    cols = st.columns(5)
    for i, m in enumerate(top):
        with cols[i]:
            genres_short = ", ".join(m.get_genres()[:2])
            st.markdown(f"""
            <div class="pick-card">
                <div class="pick-title">{m.get_title()[:22]}</div>
                <div class="pick-score">{m.get_vote_average()}/10</div>
                <div class="pick-detail">{genres_short}</div>
            </div>
            """, unsafe_allow_html=True)

    rule()

    # Random pick
    section_label("feeling lucky?")
    pick = random.choice(movies)
    display_movie_card(pick)


# Search page
#Displays the search page with search bar and results
def search_page():
    user = st.session_state.current_user
    movies = st.session_state.movies_list

    st.markdown("""
    <div class="welcome-strip" style="padding: 24px 0 20px 0;">
        <h1 style="font-size:2rem;">Find a film</h1>
        <div class="tagline">Search by title — partial names and typos work too.</div>
    </div>
    """, unsafe_allow_html=True)

    query = st.text_input("What are you looking for?", placeholder="e.g. inception, dark knight, matrix...", label_visibility="collapsed")

    if query:
        user.add_to_history(query, "Searched")
        results, match_type = search_movies(query, movies)

        if results:
            if match_type == "exact":
                st.success(f"Found it — \"{results[0].get_title()}\"")
            else:
                st.info(f"No exact match for \"{query}\", but here are {len(results)} close result(s).")

            for movie in results:
                display_movie_card(movie)
                user.add_to_history(movie.get_title(), "Viewed")

                # Rating
                if user.has_rated(movie.get_title()):
                    st.caption(f"You gave this a {user.get_rated_movies()[movie.get_title()]}/10.")
                else:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        rating = st.slider(
                            f"Your rating for {movie.get_title()}",
                            1.0, 10.0, 5.0, 0.5,
                            key=f"rate_{movie.get_title()}",
                            label_visibility="collapsed"
                        )
                    with col2:
                        if st.button("Rate it", key=f"btn_{movie.get_title()}"):
                            user.rate_movie(movie.get_title(), rating)
                            movie.add_user_rating(rating)
                            user.add_to_history(movie.get_title(), f"Rated {rating}/10")
                            st.rerun()

                # Similar films
                recs = get_recommendations(movie, movies)
                if recs:
                    with st.expander(f"Films similar to {movie.get_title()}"):
                        for r in recs[:3]:
                            st.write(f"**{r.get_title()}** ({r.get_release_date()}) — {r.get_vote_average()}/10 — {', '.join(r.get_genres())}")

                rule()
        else:
            st.warning(f"Nothing came up for \"{query}\".")
            pick = random.choice(movies)
            st.write(f"How about **{pick.get_title()}**? It's rated {pick.get_vote_average()}/10.")



#Displays all movies the user has rated
def ratings_page():
    user = st.session_state.current_user

    st.markdown("""
    <div class="welcome-strip" style="padding: 24px 0 20px 0;">
        <h1 style="font-size:2rem;">Your ratings</h1>
        <div class="tagline">Everything you've scored so far.</div>
    </div>
    """, unsafe_allow_html=True)

    rated = user.get_rated_movies()
    if not rated:
        st.write("Nothing here yet. Head to Search and rate some films to get started.")
        return

    avg = round(sum(rated.values()) / len(rated), 1)
    best = max(rated, key=rated.get)
    worst = min(rated, key=rated.get)

    col1, col2, col3 = st.columns(3)
    with col1:
        display_number(len(rated), "films rated")
    with col2:
        display_number(avg, "your average")
    with col3:
        display_number(f"{rated[best]}", f"best — {best[:18]}")

    rule()

    section_label("all ratings")
    for title, rating in sorted(rated.items(), key=lambda x: x[1], reverse=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{title}**")
        with col2:
            st.write(f"**{rating}**/10")

    rule()

    section_label("chart view")
    chart_data = pd.DataFrame({"Film": list(rated.keys()), "Rating": list(rated.values())})
    st.bar_chart(chart_data.set_index("Film"))


#Browsing page - in this section that movies are being rated
#Displays browsing options for top rated and by genre
def browse_page():
    user = st.session_state.current_user
    movies = st.session_state.movies_list

    st.markdown("""
    <div class="welcome-strip" style="padding: 24px 0 20px 0;">
        <h1 style="font-size:2rem;">Browse the collection</h1>
        <div class="tagline">Sort by rating or filter by genre.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Highest rated", "By genre"])

    with tab1:
        top = sorted(movies, key=lambda m: m.get_vote_average(), reverse=True)[:10]
        for i, m in enumerate(top, 1):
            genres = ", ".join(m.get_genres()) if m.get_genres() else "—"
            col1, col2, col3 = st.columns([0.3, 4, 0.8])
            with col1:
                st.markdown(f"#### {i}")
            with col2:
                st.write(f"**{m.get_title()}** — {genres}")
                st.caption(f"{m.get_release_date()} · popularity {m.get_popularity():.0f}")
            with col3:
                st.markdown(f"#### {m.get_vote_average()}")

            with st.expander(f"More about {m.get_title()}"):
                display_movie_card(m)
                if user.has_rated(m.get_title()):
                    st.caption(f"You rated this {user.get_rated_movies()[m.get_title()]}/10.")
                else:
                    r = st.slider("Rate", 1.0, 10.0, 5.0, 0.5, key=f"br_{m.get_title()}", label_visibility="collapsed")
                    if st.button("Submit", key=f"bbtn_{m.get_title()}"):
                        user.rate_movie(m.get_title(), r)
                        m.add_user_rating(r)
                        user.add_to_history(m.get_title(), f"Rated {r}/10")
                        st.rerun()

    with tab2:
        all_genres = sorted({g for m in movies for g in m.get_genres()})
        selected_genre = st.selectbox("Pick a genre", all_genres)

        if selected_genre:
            genre_movies = sorted(
                [m for m in movies if selected_genre in m.get_genres()],
                key=lambda m: m.get_vote_average(), reverse=True
            )
            st.write(f"**{len(genre_movies)}** films in {selected_genre}")
            for m in genre_movies:
                with st.expander(f"{m.get_title()} — {m.get_vote_average()}/10"):
                    display_movie_card(m)


# ===== DASHBOARD PAGE =====
#Dashboard that displays an overview of movie stats and user activity
def dashboard_page():
    user = st.session_state.current_user
    movies = st.session_state.movies_list
    rated = user.get_rated_movies()

    st.markdown("""
    <div class="welcome-strip" style="padding: 24px 0 20px 0;">
        <h1 style="font-size:2rem;">Your dashboard</h1>
        <div class="tagline">Stats, recommendations, and activity — all in one place.</div>
    </div>
    """, unsafe_allow_html=True)

    # =============================================
    # SECTION 1: RECOMMENDATIONS
    # =============================================
    section_label("recommended for you")

    if rated:
        recommendations = get_personalised_recommendations(user, movies)

        # Genre preferences
        genre_scores = {}
        genre_counts = {}
        for title, rating in rated.items():
            for m in movies:
                if m.get_title() == title:
                    for g in m.get_genres():
                        genre_scores[g] = genre_scores.get(g, 0) + rating
                        genre_counts[g] = genre_counts.get(g, 0) + 1
        genre_avg = {g: round(genre_scores[g] / genre_counts[g], 1) for g in genre_scores}

        col1, col2 = st.columns(2)
        with col1:
            st.write("**What you gravitate towards:**")
            pref_df = pd.DataFrame(
                sorted(genre_avg.items(), key=lambda x: x[1], reverse=True),
                columns=["Genre", "Your avg"]
            )
            st.bar_chart(pref_df.set_index("Genre"))

        with col2:
            st.write("**Films you'd probably enjoy:**")
            if recommendations:
                for i, (m, score) in enumerate(recommendations[:5], 1):
                    st.markdown(f"""
                    <div class="pick-card">
                        <div class="pick-title">{i}. {m.get_title()}</div>
                        <div class="pick-score">{m.get_vote_average()}/10</div>
                        <div class="pick-detail">{', '.join(m.get_genres())} · match score {score}</div>
                    </div>
                    """, unsafe_allow_html=True)

        if recommendations:
            rule()
            st.write("**Recommendation strength:**")
            rec_df = pd.DataFrame(
                [(m.get_title()[:22], score) for m, score in recommendations[:10]],
                columns=["Film", "Score"]
            )
            st.bar_chart(rec_df.set_index("Film"))
    else:
        st.write("Rate a few films first and your personalised picks will show up here.")
        popular = sorted(movies, key=lambda m: m.get_popularity(), reverse=True)[:5]
        st.write("**In the meantime, some popular ones to start with:**")
        for m in popular:
            st.write(f"- **{m.get_title()}** — {m.get_vote_average()}/10 (pop. {m.get_popularity():.0f})")

  #Trending and genre
    rule()
    section_label("trending & genre breakdown")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Most popular right now:**")
        trending = sorted(movies, key=lambda m: m.get_popularity(), reverse=True)[:10]
        trend_df = pd.DataFrame(
            [(m.get_title()[:22], m.get_popularity()) for m in trending],
            columns=["Film", "Popularity"]
        )
        st.bar_chart(trend_df.set_index("Film"))

    with col2:
        st.write("**Genre spread across the collection:**")
        genre_count = {}
        for m in movies:
            for g in m.get_genres():
                genre_count[g] = genre_count.get(g, 0) + 1
        genre_df = pd.DataFrame(
            sorted(genre_count.items(), key=lambda x: x[1], reverse=True),
            columns=["Genre", "Films"]
        )
        st.bar_chart(genre_df.set_index("Genre"))

    st.write("**How genres rate on average:**")
    genre_rating_sum = {}
    genre_rating_count = {}
    for m in movies:
        for g in m.get_genres():
            genre_rating_sum[g] = genre_rating_sum.get(g, 0) + m.get_vote_average()
            genre_rating_count[g] = genre_rating_count.get(g, 0) + 1
    genre_avg_data = sorted(
        [(g, round(genre_rating_sum[g] / genre_rating_count[g], 1)) for g in genre_rating_sum],
        key=lambda x: x[1], reverse=True
    )
    avg_genre_df = pd.DataFrame(genre_avg_data, columns=["Genre", "Avg rating"])
    st.bar_chart(avg_genre_df.set_index("Genre"))

#User activity section
    rule()
    section_label("your activity")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Recent actions:**")
        history = user.get_watch_history()
        if history:
            for entry in reversed(history[-12:]):
                st.markdown(f"""
                <div class="log-row">
                    <span class="log-action">{entry['action']}</span> — {entry['title']}<br>
                    <span class="log-time">{entry['time']}</span>
                </div>
                """, unsafe_allow_html=True)

            action_counts = {}
            for entry in history:
                action = entry["action"].split()[0]
                action_counts[action] = action_counts.get(action, 0) + 1
            st.write("**Action breakdown:**")
            st.bar_chart(pd.DataFrame(list(action_counts.items()), columns=["Action", "Times"]).set_index("Action"))
        else:
            st.write("No activity yet. Start exploring!")

    with col2:
        st.write("**Rating breakdown:**")
        if rated:
            rating_ranges = {"1-2": 0, "3-4": 0, "5-6": 0, "7-8": 0, "9-10": 0}
            for _, r in rated.items():
                if r <= 2: rating_ranges["1-2"] += 1
                elif r <= 4: rating_ranges["3-4"] += 1
                elif r <= 6: rating_ranges["5-6"] += 1
                elif r <= 8: rating_ranges["7-8"] += 1
                else: rating_ranges["9-10"] += 1
            st.bar_chart(pd.DataFrame(list(rating_ranges.items()), columns=["Range", "Films"]).set_index("Range"))

            st.write("**You vs. the crowd:**")
            comparison = []
            for title, user_rating in rated.items():
                for m in movies:
                    if m.get_title() == title:
                        comparison.append({"Film": title[:20], "You": user_rating, "Database": m.get_vote_average()})
                        break
            if comparison:
                st.bar_chart(pd.DataFrame(comparison).set_index("Film"))
        else:
            st.write("No ratings to show yet.")

  #Statistic section
    rule()
    section_label("collection overview")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Top 10 by rating:**")
        top_10 = sorted(movies, key=lambda m: m.get_vote_average(), reverse=True)[:10]
        st.bar_chart(pd.DataFrame(
            [(m.get_title()[:22], m.get_vote_average()) for m in top_10],
            columns=["Film", "Rating"]
        ).set_index("Film"))

    with col2:
        st.write("**Most discussed (by vote count):**")
        most_voted = sorted(movies, key=lambda m: m.get_vote_count(), reverse=True)[:10]
        st.bar_chart(pd.DataFrame(
            [(m.get_title()[:22], m.get_vote_count()) for m in most_voted],
            columns=["Film", "Votes"]
        ).set_index("Film"))

    # Release years
    year_count = {}
    for m in movies:
        if m.get_release_date():
            year_count[m.get_release_date()[:4]] = year_count.get(m.get_release_date()[:4], 0) + 1
    if year_count:
        st.write("**Films by release year:**")
        st.bar_chart(pd.DataFrame(sorted(year_count.items()), columns=["Year", "Films"]).set_index("Year"))

    # Progress
    rule()
    # section_label("your progress")
    # col1, col2, col3, col4 = st.columns(4)
    # highest = max(movies, key=lambda m: m.get_vote_average())
    # lowest = min(movies, key=lambda m: m.get_vote_average())
    # most_pop = max(movies, key=lambda m: m.get_popularity())
    # with col1:
    #     display_number(len(movies), "total films")
    # with col2:
    #     display_number(highest.get_vote_average(), f"best films — {highest.get_title()[:14]}")
    # with col3:
    #     display_number(lowest.get_vote_average(), f"lowest films— {lowest.get_title()[:14]}")
    # with col4:
    #     display_number(f"{most_pop.get_popularity():.0f}", f"popular — {most_pop.get_title()[:14]}")

    st.markdown("")
    rated_count = len(rated)
    total = len(movies)
    pct = rated_count / total if total > 0 else 0
    st.write(f"**{rated_count}** of **{total}** films rated ({pct*100:.1f}%)")
    st.progress(pct)

    if rated:
        fav_genres = {}
        for title, rating in rated.items():
            if rating >= 7:
                for m in movies:
                    if m.get_title() == title:
                        for g in m.get_genres():
                            fav_genres[g] = fav_genres.get(g, 0) + 1
        if fav_genres:
            st.write("**Your favourite genres** (from films you rated 7+):")
            st.bar_chart(pd.DataFrame(
                sorted(fav_genres.items(), key=lambda x: x[1], reverse=True),
                columns=["Genre", "Films"]
            ).set_index("Genre"))


#Admin section
#Admin panel for managing movies — add, edit, remove, save
def admin_page():
    user = st.session_state.current_user
    movies = st.session_state.movies_list
    genre_map = st.session_state.genre_map

    if not user.is_admin():
        st.error("You don't have permission to access this page.")
        return

    st.markdown("""
    <div class="welcome-strip" style="padding: 24px 0 20px 0;">
        <h1 style="font-size:2rem;">Admin panel</h1>
        <div class="tagline">Add, edit, remove films, and save changes.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add film", "Edit film", "Remove film", "View all", "Save to file"])

    # --- ADD ---
    #Admin function to add a new movie to the list
    with tab1:
        section_label("add a new film")
        new_title = st.text_input("Title", key="add_title")
        new_overview = st.text_area("Overview", key="add_overview")
        col1, col2 = st.columns(2)
        with col1:
            new_pop = st.number_input("Popularity", min_value=0.0, value=50.0, key="add_pop")
            new_release = st.date_input("Release date", key="add_date")
        with col2:
            new_va = st.slider("Rating", 1.0, 10.0, 5.0, 0.1, key="add_va")
            new_vc = st.number_input("Vote count", min_value=0, value=100, key="add_vc")
        new_poster = st.text_input("Poster path (optional)", key="add_poster")
        genre_names = sorted(set(genre_map.values()))
        new_genres = st.multiselect("Genres", genre_names, key="add_genres")

        if st.button("Add film", type="primary", key="add_btn"):
            exists = any(m.get_title().lower() == new_title.lower() for m in movies)
            if exists:
                st.error(f"\"{new_title}\" is already in the collection.")
            elif new_title:
                new_movie = Movie(new_title, new_overview, new_pop, new_poster or "N/A", str(new_release), new_va, new_vc)
                for g in new_genres:
                    new_movie.setGenre(g)
                movies.append(new_movie)
                st.success(f"Added \"{new_title}\" to the collection.")
                st.rerun()
            else:
                st.warning("A title is needed at minimum.")

    # --- EDIT ---
    #Admin function to edit an existing movie
    with tab2:
        section_label("edit a film")
        titles = [m.get_title() for m in movies]
        selected = st.selectbox("Select film", titles, key="edit_select")
        if selected:
            movie = next(m for m in movies if m.get_title() == selected)
            e_title = st.text_input("Title", value=movie.get_title(), key="e_title")
            e_overview = st.text_area("Overview", value=movie.get_overview(), key="e_overview")
            col1, col2 = st.columns(2)
            with col1:
                e_pop = st.number_input("Popularity", value=float(movie.get_popularity()), key="e_pop")
                e_release = st.text_input("Release date", value=movie.get_release_date(), key="e_release")
            with col2:
                e_va = st.slider("Rating", 1.0, 10.0, float(movie.get_vote_average()), 0.1, key="e_va")
                e_vc = st.number_input("Vote count", value=int(movie.get_vote_count()), key="e_vc")
            e_poster = st.text_input("Poster path", value=movie.get_poster_path(), key="e_poster")
            e_genres = st.multiselect("Genres", sorted(set(genre_map.values())), default=movie.get_genres(), key="e_genres")

            if st.button("Save changes", type="primary", key="e_btn"):
                movie.set_title(e_title)
                movie.set_overview(e_overview)
                movie.set_popularity(e_pop)
                movie.set_release_date(e_release)
                movie.set_vote_average(e_va)
                movie.set_vote_count(e_vc)
                movie.set_poster_path(e_poster)
                movie.genres = list(e_genres)
                st.success(f"Updated \"{e_title}\".")
                st.rerun()

    # --- REMOVE ---
    #Admin function to remove a movie from the list
    with tab3:
        section_label("remove a film")
        titles = [m.get_title() for m in movies]
        to_remove = st.selectbox("Select film to remove", titles, key="rm_select")
        if to_remove:
            movie = next(m for m in movies if m.get_title() == to_remove)
            display_movie_card(movie)
            st.warning(f"This will permanently remove \"{to_remove}\" from the collection.")
            if st.button("Yes, remove it", type="primary", key="rm_btn"):
                movies.remove(movie)
                st.success(f"Removed \"{to_remove}\".")
                st.rerun()

    # --- VIEW ALL ---
    #Admin function to view all movies in a table format
    with tab4:
        section_label(f"full collection — {len(movies)} films")
        table = [{
            "#": i, "Title": m.get_title(), "Rating": m.get_vote_average(),
            "Pop.": m.get_popularity(), "Release": m.get_release_date(),
            "Votes": m.get_vote_count(), "Genres": ", ".join(m.get_genres())
        } for i, m in enumerate(movies, 1)]
        st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

    # --- SAVE ---
    #Admin function to save changes back to the JSON file
    with tab5:
        section_label("save to file")
        st.write(f"This will overwrite `movie.json` with the current {len(movies)} films.")
        if st.button("Save now", type="primary", key="save_btn"):
            name_to_id = {v: k for k, v in genre_map.items()}
            results = []
            for m in movies:
                results.append({
                    "title": m.get_title(), "overview": m.get_overview(),
                    "popularity": m.get_popularity(), "poster_path": m.get_poster_path(),
                    "release_date": m.get_release_date(), "vote_average": m.get_vote_average(),
                    "vote_count": m.get_vote_count(),
                    "genre_ids": [name_to_id[g] for g in m.get_genres() if g in name_to_id]
                })
            try:
                with open("movie.json", "w", encoding="utf-8") as f:
                    json.dump({"results": results}, f, indent=4, ensure_ascii=False)
                st.success(f"Saved {len(results)} films to movie.json.")
            except Exception as e:
                st.error(f"Couldn't save: {e}")




#If logged in, show sidebar navigation and render the selected page
if st.session_state.logged_in:
    user = st.session_state.current_user

    with st.sidebar:
        st.markdown(f"""
        <div style="padding:16px 0 8px 0;">
            <div class="brand">Movie Recommendation System</div>
            <div class="brand-sub">film companion</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(f"Signed in as **{user.getName()}** · {'admin' if user.is_admin() else 'member'}")
        st.markdown("---")

        if st.button("Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        if st.button("Search", use_container_width=True):
            st.session_state.page = "search"
            st.rerun()
        if st.button("My ratings", use_container_width=True):
            st.session_state.page = "ratings"
            st.rerun()
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("Browse", use_container_width=True):
            st.session_state.page = "browse"
            st.rerun()

        if user.is_admin():
            st.markdown("---")
            if st.button("Admin panel", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()

        st.markdown("---")
        if st.button("Sign out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = "home"
            st.rerun()

        st.markdown("---")
        st.caption(f"{len(user.get_rated_movies())} films rated · {len(user.get_watch_history())} actions")

    # Route to the right page
    pages = {
        "home": home_page, "search": search_page, "ratings": ratings_page,
        "dashboard": dashboard_page, "browse": browse_page, "admin": admin_page
    }
    pages.get(st.session_state.page, home_page)()

#Run login page
else:
    login_page()
