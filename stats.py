import streamlit as st 


if "goal" in st.session_state:
    st.write(st.session_state.goal)

guesses_per_session = dict()
