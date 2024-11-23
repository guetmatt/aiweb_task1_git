import streamlit as st 
import pandas as pd



# page links for navigation
st.page_link("game.py", label="Guessing Game", icon="🎲")
st.page_link("stats.py", label = "Statistics", icon="🔢")


st.title("Welcome to the stats page!🔢")

# barchart of number of attempts per round
st.subheader("Number of attempts per round", divider="gray")
if "attempts_per_round" in st.session_state and len(st.session_state.attempts_per_round) > 0:
    # DataFrame for better data handling
    df_attempts = pd.DataFrame(st.session_state.attempts_per_round,
                               columns=["Attempts"])
    # index/'Rounds'-number to start from 1 instead of 0
    df_attempts.index += 1
    df_attempts.index.names = ["Rounds"]
    st.bar_chart(df_attempts,
                 x_label="Attempts", y_label="Rounds",
                 stack=True, horizontal=True)
else:
    st.write("Start playing to generate statistics!")


# average number of guessing attempts to guess goal number per round
st.subheader("Average number of attempts per round", divider="gray")
if "attempts_per_round" in st.session_state and len(st.session_state.attempts_per_round) > 0:
    st.write(f"Rounds played: {len(st.session_state.attempts_per_round)}")
    st.write(f"Average number of attempts per round: {round(sum(st.session_state.attempts_per_round) / len(st.session_state.attempts_per_round), 2)}")
else:
    st.write("Start playing to generate statistics!")


# goal numbers from previous rounds of the session
st.subheader("History of goal numbers", divider="gray")
if "goal" in st.session_state and len(st.session_state.goal_history) > 0:
    for round, goal in enumerate(st.session_state.goal_history):
        st.write(f"In round {round+1} the goal number was {goal}.")
else:
    st.write("Start playing to generate statistics!")   
