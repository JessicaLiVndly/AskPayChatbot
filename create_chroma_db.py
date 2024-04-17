from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import os
import shutil
import time

CHROMA_PATH = "chroma"
SLACK_DATA_FILE_PATH = "./slack_data/slack_sanitized.json"
# SLACK_DATA_FILE_PATH = "./slack_data/sample_data.json"
COLLECTION_NAME = "ask_pay_data"


def main():
    start = time.time()
    generate_data_store()
    stop = time.time()
    print("Elapsed time:", stop-start, "seconds")


def generate_data_store():
    documents = load_slack_history()
    chunks = split_text(documents)
    save_to_chroma(chunks)


# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata['url'] = record['url']
    return metadata


def load_slack_history():
    loader = JSONLoader(
        file_path=SLACK_DATA_FILE_PATH,
        jq_schema='.[]',
        content_key="messages",
        metadata_func=metadata_func,
        text_content=False,
    )
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # for document in chunks[:3]:
    #     print('-------------------------')
    #     print(document.page_content)
    #     print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(
        chunks,
        embedding=embedding_function,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
