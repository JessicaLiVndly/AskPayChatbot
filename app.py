import streamlit as st
from langchain.prompts import PromptTemplate

from create_chroma_db import generate_data_store
from fetch_genai_api import get_predictions
from query_data import query

prompt_template = """
Human: Use the following pieces of context to provide a 
concise answer to the question at the end but use at least summarize with 
250 words with detailed explaintions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:

"""

prompt_template = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def get_response(question):
    results = query(question)
    contexts = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = prompt_template.generate({"context": contexts, "question": question})
    answer = get_predictions(prompt, question, contexts, {"context": contexts, "question": question}, [])

    return answer


def main():
    st.set_page_config(page_title="Ask-Pay Chatbot", page_icon=":robot:")
    st.header("Ask-Pay Chatbot using GenAI API")

    user_question = st.text_input("Enter your question")

    with st.sidebar:
        st.title("Update Vector Store:")

        if st.button("Data Ingestion"):
            with st.spinner("Data Processing..."):
                generate_data_store()
                st.success("Data ingestion done")

    if st.button("Query"):
        with st.spinner("Querying..."):
            st.write(get_response(user_question))
            st.success("Query done")


if __name__ == "__main__":
    main()


