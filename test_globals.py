#!/usr/bin/env python3
from globals import prompt
from query import query
from langchain_community.llms.ollama import Ollama

def test_prompt():
    assert prompt(context="sutctx", question="sutquery") == """
    Answer the question based only on the following context:

    sutctx

    ---

    Answer the question based on the above context: sutquery
    """

