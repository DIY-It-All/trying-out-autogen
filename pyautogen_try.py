from autogen import *
import dotenv
import os

dotenv.load_dotenv()
GROQ_API = os.getenv("GROQ_API")

proxy = UserProxyAgent(name="proxy", code_execution_config={
                       "executor": "ipython-embedded"})  
config_list = [{
        "model": "llama3-70b-8192", 
        "api_key": GROQ_API, 
        "base_url": "https://api.groq.com/openai/v1"
    }]

llm_config = {
    "temperature": 0,
    "config_list": config_list,
}


agent_with_number = ConversableAgent(
    "agent_with_number",
    system_message="You are playing a game of guess-my-number. You have the "
    "number 53 in your mind, and I will try to guess it. "
    "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    llm_config=llm_config,
    # terminate if the number is guessed by the other agent
    is_termination_msg=lambda msg: "53" in msg["content"],
    human_input_mode="NEVER",  # never ask for human input
)

agent_guess_number = ConversableAgent(
    "agent_guess_number",
    system_message="I have a number in my mind, and you will try to guess it. "
    "If I say 'too high', you should guess a lower number. If I say 'too low', "
    "you should guess a higher number. ",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

result = agent_with_number.initiate_chat(
    agent_guess_number,
    message="I have a number between 1 and 100. Guess it!",
)
