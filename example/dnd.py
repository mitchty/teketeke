from rag import validated_query
from globals import models

# I know nothing about dnd I assume this is right based off some quick
# google searches sorry dnd nerds if its wrong, submit a pr if there
# is like a warlock or bar brawler or whatever as a class.
#
# Snag the data from here:
# cd data && curl -sLO https://media.wizards.com/2018/dnd/downloads/DnD_BasicRules_2018.pdf)
def test_dnd_rules():
    for model in models():
        assert validated_query(
            llm_model=model,
            question="How many classes are in the players handbook? (Answer with their names only)",
            response="cleric, fighter, rogue and wizard",
        )

        assert validated_query(
            llm_model=model,
            question="What color dragons are in the players handbook? (Answer with the color names only)",
            response="Red and Green",
        )
