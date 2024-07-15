import sys
import os

from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from embedding import embedding_function

from globals import chroma_path, prompt

def query(llm_model: str, question: str):
    # TODO make rag db pluggable somehow, future mitch problem haha
    # sucks to be future me.
    db = Chroma(persist_directory=chroma_path(), embedding_function=embedding_function())

    # Only look at results that are worthwhile k=5 just results that
    # are more sus than red Dino.
    results = db.similarity_search_with_score(question, k=5)

    # For everything we found in the RAG db, add it as context to the
    # llm query.
    #
    # TODO Use score maybe somehow?
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    chat_prompt_template = ChatPromptTemplate.from_template("""Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
""")
    chat_prompt = chat_prompt_template.format(context=context_text, question=question)


    if os.getenv("DEBUG"):
        print(chat_prompt)

    model = Ollama(model=llm_model)
    response_text = model.invoke(chat_prompt)

    # From the metadata get the id of the docs we got results from.
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"llm: {llm_model}\nresponse: {response_text}\nsources: {sources}"

    print(formatted_response)

    return response_text

def test_prompt(expect=str, actual=str):
    return """Expected Response: {expect}
    Actual Response: {actual}
    ---
    (Answer only with 'true' or 'false') Does the actual response match the expected response?
    """.format(expect=expect, actual=actual)

def validated_query(llm_model: str, question: str, response: str):
        response_text = query(llm_model=llm_model, question=question)
        queryprompt = test_prompt(expect=response, actual=response_text)
        print(queryprompt)

        model = Ollama(model=llm_model)

        # Make the result string consistent
        result = model.invoke(queryprompt).strip().lower()

        if "true" in result:
            print(f"response: {result}")
            return True
        elif "false" in result:
            print(f"response: {result}")
            return False
        else:
            raise ValueError(
                f"invalid result from llm {llm_model}. Did not reply with 'true' or 'false'.".format(llm_model=llm_model)
            )
