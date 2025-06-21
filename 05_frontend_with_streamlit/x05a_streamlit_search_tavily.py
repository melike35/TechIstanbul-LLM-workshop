import streamlit as st
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

tavily_search = TavilySearchResults()

@tool
def search_web(query: str) -> list:
    """Search the web for real-time information using Tavily."""
    return tavily_search.run(query)

st.title("🔍 AI-Powered Web Search")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Fetching results..."):
            results = search_web.run(query)
        st.success("Search Completed!")
        for result in results:
            st.subheader(result.get("title", "No Title"))
            st.write(result.get("content", "No Content"))
            st.write(f"[Link]({result.get('url', '#')})")
            st.markdown("---")
    else:
        st.warning("Please enter a query.")