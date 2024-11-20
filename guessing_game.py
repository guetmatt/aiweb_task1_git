import streamlit as st
from openai import OpenAI
import random
import time


######### CHAT FEATURE #########
st.title("ChatGPT-like clone")


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

if "number_of_guesses" not in st.session_state:
    st.session_state.number_of_guesses = 0#


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
        response = ["Hello and welcome to this guessing game! Please guess a number from 0 to 100. The possible range of numbers includes 0 and 100."]
        for word in response[0].split():
            yield word + " "
            time.sleep(0.05)
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator_init())
    st.session_state.messages.append({"role": "assitant", "content": response})
#-----------------------------------------------------------------------------------------#



def response_generator(response_number: int):
    response = [
        f"Your guess {prompt} does not match the goal number. The goal number is bigger than your guess. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Your guess {prompt} does not match the goal number. The goal number is smaller than your guess. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Congratulations, your guess {prompt} is correct! This was attempt {st.session_state.number_of_guesses}. A new number to guess has been generated.",
        "Your guess is not eligible as it is not a number in the range from 0 to 100 or it is not a number at all. This guess will not be counted towards your number of attempts. Please try again."
    ]
    for word in response[response_number].split():
        yield word + " "
        time.sleep(0.05)


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
                response = st.write_stream(response_generator(2))
            st.session_state.messages.append({"role": "assitant", "content": response})

            st.session_state.goal = random.randint(0, 100)
            st.session_state.number_of_guesses = 0

        else:
            feedback = int(goal_is_smaller(st.session_state.goal, int(prompt)))
            with st.chat_message("assistant"):
                response = st.write_stream(response_generator(feedback))
            st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(3))
        st.session_state.messages.append({"role": "assistant", "content": response})
#-----------------------------------------------------------------------------------------------#


# st.title("Let's play a guessing game!")


# if "goal" not in st.session_state:
#     st.session_state.goal = random.randint(0, 100)

# if "number_of_guesses" not in st.session_state:
#     st.session_state.number_of_guesses = 0

# with st.form("user_input_guess"):
#     guess = st.number_input("Please guess a number from 0 too 100.", min_value=0, max_value=100, value=None,
#                             placeholder="Type a number...")                    
#     st.form_submit_button("Press to guess")
    

# if type(guess) == int and guess in range(0, 101):
#     st.session_state.number_of_guesses += 1
# st.write("Number of guesses:", st.session_state.number_of_guesses)


# if guess == st.session_state.goal:
#     st.balloons()
#     st.write("Congratulations, yor guess", guess, "is correct!")
#     st.write("A new goal number has been generated.")
#     st.session_state.goal = random.randint(0, 100)
#     st.session_state.number_of_guesses = 0
# else:
#     st.write("Your guess", guess, "does not match the goal number.\nPlease try again.")

#     guess_feedback = st.checkbox("Fancy a tip?")
#     if guess_feedback:
#         try:
#             st.write(goal_is_smaller(st.session_state.goal, guess))
#         except:
#             st.write("No number guessed. Please guess a number.")    