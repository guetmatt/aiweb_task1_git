import streamlit as st


pg = st.navigation([st.Page("guessing_game.py"), st.Page("stats.py")])
pg.run()