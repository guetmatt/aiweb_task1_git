import streamlit as st

# multipage setup
pg = st.navigation([st.Page("game.py", title="Guessing Game", icon="🎲"), st.Page("stats.py", title="Statistics", icon="🔢")])
pg.run()