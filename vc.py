from langchain.text_splitter import MarkdownTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os 
from glob import glob

def load_and_chunk_documents(file_path: str) -> list[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, "sm_markdown")
    file_paths = glob(os.path.join(folder_path, "*.md"))
    
    all_chunks = []
    count = 0

    markdown_splitter = MarkdownTextSplitter (
        chunk_size = 250,
        chunk_overlap = 50
    )
    for file_path in file_paths: 
        loader = TextLoader(file_path)
        documents = loader.load()

        chunks = markdown_splitter.split_documents(documents)
        all_chunks.extend(chunks)

        count +=1
        print(f"Created {len(chunks)} chunks from {os.path.basename(file_path)}")  

    print(f"Chunked {count} files in total")
    return all_chunks 

def create_embeddings(chunks: list[str]):
    embeddings = OllamaEmbeddings(model="bge-m3")
    embedding_size = len(embeddings.embed_query("test"))
    print(f"Embedding size: {embedding_size}")

    client = QdrantClient(host="localhost", port=6333) #change to podman 

    client.create_collection(
        collection_name="rags_documents",
        vectors_config=models.VectorParams(
            size=embedding_size,
            distance=models.Distance.COSINE, 
        )
    )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rags_documents",
        embedding=embeddings, 
    )
    vector_store.add_documents(chunks)
    return vector_store

def query_documents(vector_store: QdrantVectorStore, query: str, k: int = 3) -> list[str]: 
    results = vector_store.similarity_search(query, k = k)
    return [doc.page_content for doc in results]

def main():
    chunks = load_and_chunk_documents(file_path= str) 
    print(f"Created {len(chunks)} chunks")
    
    vector_store = create_embeddings(chunks)
    print("embeddings created and stored in Qdrant")

    query = "What is K9VB's name?"
    results = query_documents(vector_store, query)

    print("\nQuery:", query)
    print("\nTop 3 matches:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}, {result[:500]}...")
if __name__ == "__main__":
    main()