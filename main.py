import os
import json
import subprocess
from dotenv import load_dotenv
from tools import make_tools
from db import new_client
from google import genai
from google.genai import types
from datetime import date
from getpass import getpass


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY") 


if not api_key : 
    raise ValueError("No API key found.")

gemini = genai.Client(api_key=api_key)
MODEL = "gemini-3.1-flash-lite" #changed it to 3.1 when error 503 is the result. regular base is 3.5


SYSTEM_PROMPT = (
    "You are an academic assistant for students. "
    f"Today is {date.today().strftime('%A')}, {date.today()}. "
    "When the user gives a file path to their syllabus, read it with read_syllabus, "
    "then save every assignment and exam you find with add_assignment, one call each. "
    "Convert relative dates like 'next Monday' or 'in two weeks' into YYYY-MM-DD "
    "using today's date, and tell the user the exact date you saved so they can correct it. "
    "If a date or course name is unclear, ask the user instead of guessing. "
    "When the user asks what is due, use list_assignments. "
    "If a tool returns success: False, tell the user its message."
)



def build_config(tools):
    return types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=tools,
    )



def run_agent(messages, config) :
    response = gemini.models.generate_content(
        model= MODEL, contents = messages, config=config
    )
    
    return(response.text)


def main():
    db_client = new_client()
    email = input("Please enter your email: ")
    password = getpass("Please enter your password: ")

    try:
        db_client.auth.sign_in_with_password({"email": email, "password":password})
    except Exception:
        print("Login failed. Check your email and password.")
        return
    config = build_config(make_tools(db_client))
    messages = [] #this allows our agent to remember the conversation and not forget it after one input.
    print ("Hi! Today is " + str(date.today().strftime('%A'))+ ", I am your academic assistant: what do you need assistance with? ")
    while True: #this allows the user to keep entering prompts.
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break
        
        messages.append({"role": "user", "parts": [{"text": user_input}]}) #we take their user input and add to messsages. 
        bot_reply = run_agent(messages, config) #we run the agent. so we keep going until user does quit. 
        messages.append({"role": "model", "parts": [{"text": bot_reply}]}) 
        print(f"\nAgent: {bot_reply}")

if __name__ == "__main__":
    main()
