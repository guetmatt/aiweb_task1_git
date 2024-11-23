import streamlit as st
from openai import OpenAI
import random
import time

## Access to OpenAI -- played around with it, but not needed for application
# set OpenAI API key from Streamlit secrets
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# # set OpenAI model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-4o-mini"


#-----------------#
#--- Functions ---#
#-----------------#

def setup_game():
    """Set up the game when loading the webpage.
    Initialize goal number, data structures for statistics, etc.
    """
    if "goal" not in st.session_state:
        st.session_state.goal = random.randint(0, 100)
    
    if "goal_history" not in st.session_state:
        st.session_state.goal_history = list()

    if "number_of_guesses" not in st.session_state:
        st.session_state.number_of_guesses = 0

    if "attempts_per_round" not in st.session_state:
        st.session_state.attempts_per_round = list()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def restart():
    """Restart the current guessing round by generating
    a new goal number and resetting the number of guesses.
    """
    st.session_state.goal = random.randint(0, 100)
    st.session_state.number_of_guesses = 0


def save_stats():
    """Save statistics of a guessing round."""
    st.session_state.attempts_per_round.append(st.session_state.number_of_guesses)
    st.session_state.goal_history.append(st.session_state.goal)


def goal_is_smaller(goal: int, guess: int):
    """Compare goal number and guessing number.
    
    :param goal (int): goal number
    :param guess (int): guess number
    :return (bool): boolean whethter goal number is smaller than guessing number 
    """
    if goal < guess:
        return True
    else:
        return False
    

# response generator for chatbot
# contains all possible responses of chatbot
# 'response_number' 
prompt = "initial_placeholder"
def response_generator(response_number: int):
    """Response generator for function 'message_from_chatbot'.
    Contains all possible responses of chatbot.

    :param response_number (int): index to choose the response to be generated
    """
    response = [
        f"Close! The goal number is slightly bigger than your guess '{prompt}'. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Close! The goal number is slightly smaller than your guess '{prompt}'. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Your guess '{prompt}' does not match the goal number. The goal number is bigger than your guess. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Your guess '{prompt}' does not match the goal number. The goal number is smaller than your guess. This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Whoops! Your guess '{prompt}' is waaaay smaller than the goal number.  This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Whoops! Your guess '{prompt}' is waaaay bigger than the goal number.  This was attempt {st.session_state.number_of_guesses}. Please try again.",
        f"Congratulations, your guess '{prompt}' is correct! This was attempt {st.session_state.number_of_guesses}. A new number to guess has been generated.",
        f"Your guess '{prompt}' is not eligible as it is not a number in the range from 0 to 100 or it is not a number at all. This guess will not be counted towards your number of attempts. Please try again.",
        f"A new goal number has been generated. The number to guess was {st.session_state.goal}.",
        "Hello and welcome to this guessing game! Please guess a number from 0 to 100. The possible range of numbers includes 0 and 100. If you want to generate a new goal number while still guessing, type 'restart'."
    ]
    
    # 'typing effect' for chatbot response
    for word in response[response_number].split():
        yield word + " "
        time.sleep(0.03)
    

def message_from_chatbot(index: int):
    """Generates a message by the chatbot.

    :param index (int): index to choose the response to be generated
    """
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(index))
    st.session_state.messages.append({"role": "assistant", "content": response})


def initial_message_from_chatbot():
    """Generates initial message by chatbot when loading the webpage."""
    if "initial_message" not in st.session_state:
        st.session_state.initial_message="init"
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(-1))
        st.session_state.messages.append({"role": "assitant", "content": response})



#---------------------#
#--- Guessing Game ---#
#---------------------#


# initialize game session and chatbot
st.title("🎲Guessing Game")
setup_game()
initial_message_from_chatbot()

# user input field for communication with chatbot
if prompt := st.chat_input("What is up?", key="input_main"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # case: user input is a valid guess (integer in intervall [0, 100])
    if prompt.isdigit() and int(prompt) in range(0, 101):
        # count user input as a valid guess
        st.session_state.number_of_guesses += 1

        # subcase: user guessed the goal number
        # - congrats, save some statistics, start new round
        if int(prompt) == st.session_state.goal:
            st.balloons()
            message_from_chatbot(6)
            save_stats()
            restart()
        
        # subcase: user guessed wrong number
        else:
            # generate feedback response based on
            # distance between goal number and user guess 
            distance = abs(int(prompt) - st.session_state.goal)
            distance_range = [range(1,11), range(11,36), range(36, 101)]
            feedback = int(goal_is_smaller(st.session_state.goal, int(prompt)))
            for index, dist_range in enumerate(distance_range):
                if distance in dist_range:
                    answer_index = index*2 + feedback
            message_from_chatbot(answer_index)

    # case: user wants to restart guessing round
    elif prompt.lower() == "restart":
        message_from_chatbot(8)
        restart()

    # case: user input is not valid (not an integer in intervall [0, 100])
    else:
        message_from_chatbot(7)