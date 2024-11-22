import streamlit as st 
import pandas as pd


st.title("Welcome to the statistics page!")


st.subheader("Number of attempts per round", divider="gray")
if "attempts_per_round" in st.session_state and len(st.session_state.attempts_per_round) > 0:
    df_attempts = pd.DataFrame(st.session_state.attempts_per_round,
                               columns=["Attempts"])
    df_attempts.index += 1
    df_attempts.index.names = ["Rounds"]
    st.bar_chart(df_attempts,
                 x_label="Attempts", y_label="Rounds",
                 stack=True, horizontal=True)
else:
    st.write("Start playing to generate statistics!")


st.subheader("Average number of attempts per round", divider="gray")
if "attempts_per_round" in st.session_state and len(st.session_state.attempts_per_round) > 0:
    st.write(f"You played {len(st.session_state.attempts_per_round)} rounds with an average of {round(sum(st.session_state.attempts_per_round) / len(st.session_state.attempts_per_round), 2)} attempts.")
else:
    st.write("Start playing to generate statistics!")


st.subheader("History of goal numbers", divider="gray")
if "goal" in st.session_state and len(st.session_state.goal_history) > 1:
    for round, goal in enumerate(st.session_state.goal_history[:-1]):
        st.write(f"In round {round+1} the goal number was {goal}.")
else:
    st.write("Start playing to generate statistics!")   
