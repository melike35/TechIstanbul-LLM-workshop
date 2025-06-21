## Environment Setup:
Ensure your .env file includes a TAVILY_API_KEY. You’ll need to sign up for Tavily (https://tavily.com/) to get an API key. Your .env might look like:
- env
```python
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```
## Copy chromadb directory from 03 to 04

## Retreiver
-
```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma(
    collection_name="italia-guide",
    embedding_function=embeddings,
    persist_directory="./chromadb", 
)
```

## LLM with tools
- x04_adding_external_tool.py
```python
from x03a_document_ingestion_to_vectordb import vector_store
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents.agent_toolkits import create_retriever_tool, create_conversational_retrieval_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.tools import TavilySearchResults  # Import Tavily search tool
from dotenv import load_dotenv

# Load environment variables (e.g., OpenAI API key, Tavily API key)
load_dotenv()

# Set up the retriever from the vector store
retriever = vector_store.as_retriever()

# Create a retriever tool for Italy travel data
italy_travel_retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="italy_travel",
    description="Searches and returns documents regarding Italy."
)

# Create the Tavily web search tool
tavily_search_tool = TavilySearchResults(
    name="tavily_search",
    description="Searches the web for current information using Tavily."
)

# Combine both tools into a list
tools = [italy_travel_retriever_tool, tavily_search_tool]

# Set up conversation memory
memory = ConversationBufferMemory(
    chat_memory=ChatMessageHistory(),
    memory_key='chat_history',
    return_messages=True
)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create the conversational retrieval agent
agent_executor = create_conversational_retrieval_agent(
    llm=llm,
    tools=tools,
    memory_key='chat_history',
    verbose=True
)

if __name__ == '__main__':
    # Invoke the agent with a question
    response = agent_executor.invoke({"input": "Where can I visit in Istanbul in 1 day?"})
    print(response)
```