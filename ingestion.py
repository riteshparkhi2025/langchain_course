import asyncio
import os
import ssl
from typing import Any, Dict,List

import certifi
from dotenv import load_dotenv

load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap

from logger import (Colors, log_error, log_header, log_info, log_success, log_warning)


# Configure SLL Context to use certifi certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_CA_BUNDLE"] = certifi.where()


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", show_progress_bar=True, chunk_size=50, retry_min_seconds=10
)

#croma = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
vectorstore = PineconeVectorStore(index_name="langchain-doc-index", embedding=embeddings)
tavily_extract = TavilyExtract()
tavily_map=TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl =TavilyCrawl()


async def index_documents_async(documents: List[Document], batch_size: int = 50):
    """Process documents in batches asynchronously"""
    log_header("VECTOR STORAGE PHASE")
    log_info(f"Vector Store Indexing: Preparing to add {len(documents)} documnents to vector store",
             Colors.DARKCYAN)

    # Create baches
    batches = [
        documents[i: i + batch_size] for i in range(0, len(documents), batch_size)
    ]

    log_info(f"VectorStore Indexing: Split into {len(documents)} baches of {batch_size} documents each")


    # Prcoess all batches concurrently
    async def add_batch(batch: List[Document], batch_num:int):
        try:
            await vectorstore.aadd_documents(batch)
            log_success(f"VectorStore Indexing: Successfully added batch {batch_num}/{len(batch)} documents")
        except Exception as e:
            log_error(f"VectorStore Indexing: Failed to add batch {batch_num} - {e}")
            return False
        return True

    # Process batches concurrently
    tasks =[add_batch(batch, i + 1) for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks,return_exceptions=True)

    # Count successful batches
    successful = sum(1 for result in results if result is True)
    if successful == len(batches):
        log_success(f"VectorStore Indexing: All batches processed successfully! ({successful}/{len(batches)})")
    else:
        log_warning(f"VectorStore Indexing: Processed {successful}/{len(batches)}")





async def main():
    """Main async function to orchestrate the entire process."""
    log_header("DOCUMENENTATION INGESTION PIPELINE")

    log_info("TavilyCrawl: Starting to Crawl documentation from https://python.langchain.com/", Colors.PURPLE)

    # Crawl the documentation site
    res = tavily_crawl.invoke({
        "url": "https://python.langchain.com/",
        "max_depth": 3,
        "extract_depth": "advanced",
        #"instructions":"content on ai agents"
    })
    all_docs = []
    skipped_results = 0
    for result in res["results"]:
        raw_content = result.get("raw_content")
        if not isinstance(raw_content, str):
            skipped_results += 1
            continue
        all_docs.append(
            Document(page_content=raw_content, metadata={"source": result["url"]})
        )

    if skipped_results:
        log_warning(
            f"TavilyCrawl: Skipped {skipped_results} results without string content"
        )
    log_success(
        f"TavilyCrawl: Created documents from {len(all_docs)} crawled URLs"
    )


    #Split documents into chunks
    log_header("DOCUMENT CHUNKING PHASE")
    log_info(f"Text splitter: Processing {len(all_docs)} documents with 4000 chunk size and 200 overlap",
             Colors.YELLOW)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    splitted_docs = text_splitter.split_documents(all_docs)
    log_success(f"Text Splitter: Created {len(splitted_docs)} chunks from {len(all_docs)} documents")

    #Process documents asynchronously
    await index_documents_async(splitted_docs, batch_size=500)

    log_header("PIPELINE COMPLETED")
    log_success("Documention ingesion pipeline finished successfully")
    log_info(" Summary", Colors.BOLD)
    log_info(f" URLs crawled: {len(res['results'])}")
    log_info(f" Documents extraction:{len(all_docs)}")
    log_info(f"Chunks created: {len(splitted_docs)}")



if __name__ == "__main__":
    asyncio.run(main())