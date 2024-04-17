import json

import chromadb
import argparse

CHROMA_PATH = "chroma"
COLLECTION_NAME = "ask_pay_data"

PROMPT_TEMPLATE = """
Answer the question based only on the following context. Do not make up the answer:

{context}

---

Answer the question based on the above context: {question}
"""


def get_chroma_collection():
    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    return chroma_client.get_collection(COLLECTION_NAME)


def query_data(query_text):
    # grab the collection
    collection = get_chroma_collection()

    # Search the DB.
    results = collection.query(query_texts=query_text, n_results=3)
    if len(results) == 0:
        print(f"Unable to find matching results.")
        return [], {}

    docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    sources = {item['url'] for item in metadatas}
    return docs, sources


def main():
    query_text = input("Enter your question: ")
    docs, sources = query_data(query_text)

    print(docs)
    print(sources)

    # query the AI model
    # context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, question=query_text)
    #
    # model = ChatOpenAI()
    # response_text = model.predict(prompt)
    #
    # sources = [doc.metadata.get("source", None) for doc, _score in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)


if __name__ == "__main__":
    main()
