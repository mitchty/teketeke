from rag import validated_query
from globals import models

# Snag the data for this from here and load into chromadb
# (cd data && curl -sLO https://www.apple.com/newsroom/pdfs/fy2024-q1/FY24_Q1_Consolidated_Financial_Statements.pdf)
def test_apple():
    for model in models():
        assert validated_query(
            llm_model=model,
            question="What was the net income for the operating months ending in 2023 (Answer only with the number)",
            response="$33,916",
        )
