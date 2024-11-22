import streamlit as st


pg = st.navigation([st.Page("Guessing_Game.py"), st.Page("Statistics.py")])
pg.run()