from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import argparse

load_dotenv()

chat = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
"""
# 
system_prompt = "You are a helpful assistant that helps the user to plan an optimized itinerary."
user_question = "I'm going to Istanbul for 2 days, offer me top 5 places to visit?"

response = chat.invoke([
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_question)
])

print("Response:", response.content)
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chat with OpenAI model using LangChain.")
    parser.add_argument("--system", type=str, required=True, help="You are a helpful assistant that help the user to plan an optimized itinerary.")
    parser.add_argument("--question", type=str, required=True, help="I'm going to Istanbul for 2 days, offer me top 5 places to visit?")
    args = parser.parse_args()

    response = chat.invoke([
        SystemMessage(content=args.system),
        HumanMessage(content=args.question)]
        )
    print("Response:", response.content)