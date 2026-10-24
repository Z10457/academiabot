import os
import json
import subprocess
from dotenv import load_dotenv
#import TOOLS
#import TOOL_SCHEMAS

from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") 


if not api_key : 
    raise ValueError("No API key found.")

client = genai.Client(api_key=api_key)
MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = "insent prompt here, what the language will do. " 

#now we will list the tools and commands that we will use. 
#THE MORE tools we have, the better it will perform. 

TOOL_SCHEMAS = [
    {#we can have the llm call any tool, so we can make any project one really wants. 
    }
]

def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print (f" tool: {name}({args})")
    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}" #if there is an error, it will tell us the error instead of just failing. 

def run_agent(messages) :

    while True:
        print("Running agent...")
        response = client.models.generate_content(
            model=MODEL,
            contents = messages,
            
        )
        print("Gemini responded")
        return(response.text)


def main():
    messages = [] #this allows our agent to remember the conversation and not forget it after one input.
    print ("Hi! I am your academic assistant: what do you need assistance with? ")
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
