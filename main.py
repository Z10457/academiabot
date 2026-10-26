import os
import json
import subprocess
from dotenv import load_dotenv
from tools import add_assignment
from google import genai
from google.genai import types
from datetime import date

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") 


if not api_key : 
    raise ValueError("No API key found.")

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = {f"Today is {date.today()}. "}

config = types.GenerateContentConfig( #this creates config.
    system_instruction=SYSTEM_PROMPT,
    tools = [add_assignment], 
)



def run_agent(messages) :

    while True:
        print("Running agent...")
        response = client.models.generate_content(
            model=MODEL,
            contents = messages,
            config = config
        )
        return(response.text)


def main():
    messages = [] #this allows our agent to remember the conversation and not forget it after one input.
    print ("Hi! Today is " + str(date.today())+ ", I am your academic assistant: what do you need assistance with? ")
    while True: #this allows the user to keep entering prompts.
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break
        
        messages.append({"role": "user", "parts": [{"text": user_input}]}) #we take their user input and add to messsages. 
        bot_reply = run_agent(messages) #we run the agent. so we keep going until user does quit. 
        messages.append({"role": "model", "parts": [{"text": bot_reply}]}) 
        print(f"\nAgent: {bot_reply}")

if __name__ == "__main__":
    main()
