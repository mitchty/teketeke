#!/usr/bin/env python3
from langchain_community.embeddings.ollama import OllamaEmbeddings

def embedding_function():
    """
    embedding_function returns the ollama embedding function to use
    for embedding documents into the RAG.

    :return: OllamaEmbedding model used for document generation.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings
