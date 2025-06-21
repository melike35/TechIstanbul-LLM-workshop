from x03a_document_ingestion_to_vectordb import vector_store

if __name__=='__main__':
    results = vector_store.similarity_search(
    "What is best to see in Rome?",
    k=2
    )
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")