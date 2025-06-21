from langchain.chains import LLMChain, ConversationChain
from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain

from dotenv import load_dotenv

load_dotenv()


chat = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=chat, verbose=True, memory=memory)

if __name__=='__main__':
    while True:
        query = input('You: ')
        if query == 'q':
            break
        output = conversation.invoke({"input": query})
        print('User: ', query)
        print('AI system: ', output['response'])