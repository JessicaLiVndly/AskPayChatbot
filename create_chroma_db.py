from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from chromadb.utils import embedding_functions
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import os
import shutil

CHROMA_PATH = "chroma"
SLACK_DATA_FILE_PATH = "./slack_data/sample.json"
COLLECTION_NAME = "ask_pay_data"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_slack_history()
    chunks = split_text(documents)
    save_to_chroma(chunks)


# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    # TODO: populate the metadata with slack URLs here
    print(f'Record: {record}')
    return metadata


def load_slack_history():
    loader = JSONLoader(
        file_path=SLACK_DATA_FILE_PATH,
        jq_schema='.data[]',
        # content_key="content",
        metadata_func=metadata_func,
        text_content=False,
    )
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[0]
    print(document.page_content)
    print(document.metadata)

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
