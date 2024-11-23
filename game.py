import streamlit as st
from openai import OpenAI
import random
import time


######### CHAT FEATURE #########
st.title("🎲Guessing Game")


## SETUP

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Start guessing game
if "goal" not in st.session_state:
    st.session_state.goal = random.randint(0, 100)

if "goal_history" not in st.session_state:
    st.session_state.goal_history = list()
    st.session_state.goal_history.append(st.session_state.goal)

if "number_of_guesses" not in st.session_state:
    st.session_state.number_of_guesses = 0

if "attempts_per_round" not in st.session_state:
    st.session_state.attempts_per_round = list()


def goal_is_smaller(goal: int, guess: int):
    if goal < guess:
        return True
    else:
        return False
#-------------------------------------------------------#



# Generate initial message from chatbot

if "initial_message" not in st.session_state:
    st.session_state.initial_message="init"

    def response_generator_init():
        response = ["Hello and welcome to this guessing game! Please guess a number from 0 to 100. The possible range of numbers includes 0 and 100. If you want to generate a new goal number while still guessing, type 'restart'."]
        for word in response[0].split():
            yield word + " "
            time.sleep(0.01)
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator_init())
    st.session_state.messages.append({"role": "assitant", "content": response})
#-----------------------------------------------------------------------------------------#



def response_generator(response_number: int):
    response = [
        f"Close! The goal number is slightly bigger than your guess '{prompt}'. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Close! The goal number is slightly smaller than your guess '{prompt}'. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Your guess '{prompt}' does not match the goal number. The goal number is bigger than your guess. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Your guess '{prompt}' does not match the goal number. The goal number is smaller than your guess. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Whoops! Your guess '{prompt}' is waaaay smaller than the goal number.  This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Whoops! Your guess '{prompt}' is waaaay bigger than the goal number.  This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Congratulations, your guess '{prompt}' is correct! This was attempt {st.session_state.number_of_guesses}. A new number to guess has been generated.",
        f"Your guess '{prompt}' is not eligible as it is not a number in the range from 0 to 100 or it is not a number at all. This guess will not be counted towards your number of attempts. Please try again.",
        f"A new goal number has been generated. The number to guess was {st.session_state.goal}."
    ]
    for word in response[response_number].split():
        yield word + " "
        time.sleep(0.01)


# User number guess
if prompt := st.chat_input("What is up?", key="input_main"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.isdigit() and int(prompt) in range(0, 101):
        st.session_state.number_of_guesses += 1
        if int(prompt) == st.session_state.goal:
            st.balloons()

            with st.chat_message("assistant"):
                response = st.write_stream(response_generator(6))
            st.session_state.messages.append({"role": "assitant", "content": response})

            st.session_state.attempts_per_round.append(st.session_state.number_of_guesses)
            st.session_state.goal = random.randint(0, 100)
            st.session_state.goal_history.append(st.session_state.goal)
            st.session_state.number_of_guesses = 0

        else:
            distance = abs(int(prompt) - st.session_state.goal)
            distance_range = [range(1,11), range(11,36), range(36, 101)]
            feedback = int(goal_is_smaller(st.session_state.goal, int(prompt)))
            for index, dist_range in enumerate(distance_range):
                if distance in dist_range:
                    answer_index = index*2 + feedback
            with st.chat_message("assistant"):
                response = st.write_stream(response_generator(answer_index))
            st.session_state.messages.append({"role": "assistant", "content": response})

    elif prompt.lower() == "restart":
        with st.chat_message("assistant"):
                response = st.write_stream(response_generator(8))
        st.session_state.messages.append({"role": "assitant", "content": response})
        
        st.session_state.goal = random.randint(0, 100)
        st.session_state.number_of_guesses = 0

    else:
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(7))
        st.session_state.messages.append({"role": "assistant", "content": response})