from x03a_document_ingestion_to_vectordb import vector_store
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from dotenv import load_dotenv


retriever = vector_store.as_retriever()


memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Create the ConversationalRetrievalChain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

if __name__=='__main__':
    answer = qa_chain.invoke({'question':'Give me some review about the Pantheon'})
    print(answer)