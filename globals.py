import os

# junk that didn't fit elsewhere really

# Sue me I prefer functions blame functional programming languages.
#
# Goal here is to constrain the prompt in a way where it'll be
# consistent, or more consistent.
def prompt(context=str, question=str):
    return """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """.format(context=context, question=question)

def chroma_path():
    return os.getenv("CHROMA_PATH", default="chroma")

def data_path():
    return os.getenv("DATA_PATH", default="data")

def models():
    return os.environ.get('MODELS', 'mistral').split(" ")
