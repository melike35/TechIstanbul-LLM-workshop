from chroma_retriever import vector_store  # Your Chroma vector store
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents.agent_toolkits import create_retriever_tool, create_conversational_retrieval_agent
from langchain_community.tools import TavilySearchResults
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage

# --- For the ReAct Agent ---
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom callback handler for streaming
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Streamlit page configuration
st.set_page_config(page_title="GlobeBotter")
st.header("Welcome to Globebotter, your travel assistant with Internet access. What are you planning for your next trip?")

# Set up the retriever from the imported Chroma vector store
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# Create retriever tool for Italy travel data
italy_travel_retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="italy_travel",
    description="Searches and returns travel documents regarding Italy from a Chroma vector store."
)

# Set up Tavily search tool
tavily_search = TavilySearchResults(
    name="tavily_search",
    description="Searches the web for real-time travel information using Tavily."
)

# Define tools list
tools = [italy_travel_retriever_tool, tavily_search]

# Set up conversation memory
memory = ConversationBufferMemory(
    chat_memory=ChatMessageHistory(),
    memory_key='chat_history',
    return_messages=True
)

# Initialize LLM with error handling
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
except Exception as e:
    print(f"Error initializing LLM: {e}")
    exit(1)

# --- AGENT CREATION ---
# 1. Get the ReAct prompt template
# This prompt contains instructions on how the LLM should use tools and format its thoughts.
prompt = hub.pull("hwchase17/react-chat")

# 2. Create the ReAct agent
# This agent is designed to handle multiple tools and their outputs more effectively.
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Create the conversational retrieval agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True # Handles cases where the LLM output isn't perfect
)

# Streamlit UI
user_query = st.text_input(
    "**Where are you planning your next vacation?**",
    placeholder="Ask me anything!"
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
if "memory" not in st.session_state:
    st.session_state["memory"] = memory

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

def display_msg(msg, author):
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

if user_query:
    display_msg(user_query, 'user')
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke({"input": user_query}, callbacks=[st_cb])
        output = response.get("output", "No response generated.")
        st.write(output) 

if st.sidebar.button("Reset chat history"):
    st.session_state.messages = []
    st.session_state["memory"].clear()