#!/usr/bin/env python3
#import argparse
import sys
import os

from rag import query
from globals import models

def main():
    query_text = " ".join(sys.argv[1:])

    for model in models():
        query(model, query_text)

if __name__ == "__main__":
    main()
