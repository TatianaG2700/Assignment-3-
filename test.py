import streamlit as st

st.title("Simple Info App")

name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

if name and age:
    st.write(f"Hello {name}! You are {int(age)} years old.")
    st.write(f"In 5 years, you'll be {int(age) + 5}.")
