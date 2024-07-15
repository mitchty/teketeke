#!/usr/bin/env python3
import os
import shutil

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from embedding import embedding_function

from globals import chroma_path, data_path

def main():
    documents = PyPDFDirectoryLoader(data_path()).load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    ).split_documents(documents)
    repopulate(chunks)

def repopulate(chunks: list[Document]):
    """
    repopulate
    
    For now just uses chroma and an embed model to split/save the data into a vector db.

    :param chunks: list of Documents to add to the chroma db
    :return: None
    """
    db = Chroma(persist_directory=chroma_path(), embedding_function=embedding_function())

    chunknames = gen_chunknames(chunks)

    existing = set(db.get(include=[])["ids"])
    print(f"Rag DB contains {len(existing)} document chunks")

    # TODO How do I handle versioning of chunks or docs if a duplicate
    # doc is inserted? sha256sum of each chunk contents or doc itself?
    # Future mitch problem as is tradition. Eat it future me!
    add = []
    for chunk in chunknames:
        if chunk.metadata["id"] not in existing:
            add.append(chunk)

    if len(add):
        print(f"adding {len(add)} new documents to rag db")
        add_ids = [chunk.metadata["id"] for chunk in add]
        db.add_documents(add, ids=add_ids)
        db.persist()
    else:
        print("nothing to do")


def gen_chunknames(chunks):
    """
    gen_chunknames

    Take a list of Documents and chunk them into unique/consistent names into chromadb

    E.g. for data/example.pdf an id of:
    data/example.pdf:PAGE#:CHUNKINDEX

    Is returned to ensure unique names. TODO is to make the name tied to either the input data checksum or the chunk checksum. But that makes the names insanely long when I tried so for now its simple.

    :param chunks: list[Document] inputs to be chunked into chroma db
    :return: list[Document]
    """
    last = None
    curr = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        idx = f"{source}:{page}"

        if idx == last:
            curr += 1
        else:
            curr = 0

        last = idx

        chunk.metadata["id"] = f"{idx}:{curr}"

    return chunks

if __name__ == "__main__":
    main()
