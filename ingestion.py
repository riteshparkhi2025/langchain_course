import os
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pydantic import SecretStr

load_dotenv()

if __name__ == '__main__':

    # Load the documents from the "data" folder
    loader = UnstructuredLoader(os.path.join(os.path.dirname(__file__), "data", "mediumblog1.txt"),
                                chunking_strategy="basic", max_characters = 10000000, autodetect_encoding=True)
    documents = loader.load()

    print("splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks.")

    api_key = os.environ.get("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(api_key=SecretStr(api_key) if api_key else None)

    print("Ingesting...")

    PineconeVectorStore.from_documents(docs, embeddings, index_name=os.environ.get("INDEX_NAME"))
    print("Ingestion complete.")