# Ingest data to vectorstore
- Add langchain_chroma to requirements.txt
## 1. Load pdfs
#### Copy pdfs folder 
- x03a_document_ingestion_to_vectordb.py

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

# Read pdf content
raw_documents = PyPDFDirectoryLoader(path="pdfs").load()

# Split raw pdf content into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

split_documents = text_splitter.split_documents(raw_documents)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma(
    collection_name="italia-guide",
    embedding_function=embeddings,
    persist_directory="./chromadb", 
)

# Add items to vector store
uuids = [str(uuid4()) for _ in range(len(split_documents))]

vector_store.add_documents(documents=split_documents, ids=uuids)

if __name__=='__main__':
    print(type(raw_documents))
    # <class 'list'>
    print(raw_documents[:3])
```

#### Run and see pdfs
```python
 python x03a_document_ingestion_to_vectordb.py
```

## 2. Split raw pdf content into chunks
-  03_adding_non-parametric_knowledge.py
```python
...
...
# Split raw pdf content into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)
split_documents = text_splitter.split_documents(raw_documents)

if __name__=='__main__':
    #print(type(raw_documents))
    # <class 'list'>
    #print(raw_documents[:3])
    #print(len(raw_documents))
    # 21
    print(len(split_documents))
    # 111
    print(split_documents[:5])
```
#### Run
```python
 python x03a_document_ingestion_to_vectordb.py
```
## 3. Ingest documents to vectorDB
- 03a_document_ingestion_to_vectordb.py
```python
...
...
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(
    collection_name="italia-guide",
    embedding_function=embeddings,
    persist_directory="./chromadb", 
)

# Add items to vector store
uuids = [str(uuid4()) for _ in range(len(split_documents))]

vector_store.add_documents(documents=split_documents, ids=uuids)

if __name__=='__main__':
    print(type(raw_documents))
    # <class 'list'>
    #print(raw_documents[:3])
    #print(len(raw_documents))
    # 21
    # print(len(split_documents))
    # # 111
    # print(split_documents[:5])
```
#### Run
```python
python x03a_document_ingestion_to_vectordb.py
```
#### Observation:
- directory created for vectordb
- Inside directory sqlite database

# Query vector store
- x03b_query_vector_store.py
```python
from x03a_document_ingestion_to_vectordb import vector_store

if __name__=='__main__':
    results = vector_store.similarity_search(
    "What is best to see in Rome?",
    k=2
    )
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")
```
- See the query result

# 3. Feed knowledge to LLM
- x03c_feed_context_to_llm.py
```python
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
```