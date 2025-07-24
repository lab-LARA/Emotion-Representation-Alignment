import re
import os
import pandas as pd

"""
THIS SCRIPT FIXES PUNCTUATION AND CONTRACTION ISSUES IN OUTPUT TEXT. 

RUN THIS AFTER GENERATING THE QUESTIONS VIA gen_questions.py.

BEFORE RUNNING THIS, UPDATE genqus_path TO THE LOCATION OF GENERATED QUESTIONS.
"""

genqus_path = os.path.join("..", "data", "generated_questions_gpt4_reemojied")


def replace_apostrophes(text):
    # Common contractions
    contractions = [
        r'\b(Im)\b', r'\b(Ive)\b', r'\b(Id)\b', r'\b(Ill)\b', r'\b(Itd)\b',
        r'\b(Youd)\b', r'\b(Youre)\b', r'\b(Youve)\b', r'\b(Youll)\b',
        r'\b(Hes)\b', r'\b(Shes)\b', r'\b(Its)\b', r'\b(Thats)\b', r'\b(Theres)\b',
        r'\b(Wasnt)\b', r'\b(Werent)\b', r'\b(Hasnt)\b', r'\b(Havent)\b', r'\b(Hadnt)\b',
        r'\b(Wont)\b', r'\b(Wouldnt)\b', r'\b(Dont)\b', r'\b(Doesnt)\b', r'\b(Didnt)\b',
        r'\b(Cant)\b', r'\b(Couldnt)\b', r'\b(Shouldnt)\b', r'\b(Mightnt)\b', r'\b(Mustnt)\b',
        r'\b(youd)\b', r'\b(youre)\b', r'\b(youve)\b', r'\b(youll)\b',
        r'\b(hes)\b', r'\b(shes)\b', r'\b(its)\b', r'\b(thats)\b', r'\b(theres)\b',
        r'\b(wasnt)\b', r'\b(werent)\b', r'\b(hasnt)\b', r'\b(havent)\b', r'\b(hadnt)\b',
        r'\b(wont)\b', r'\b(wouldnt)\b', r'\b(dont)\b', r'\b(doesnt)\b', r'\b(didnt)\b',
        r'\b(cant)\b', r'\b(couldnt)\b', r'\b(shouldnt)\b', r'\b(mightnt)\b', r'\b(mustnt)\b',
        r'\b(cats)\b', r'\b(semesters)\b'
    ]

    # Replace contractions
    for contraction in contractions:
        text = re.sub(contraction, lambda m: m.group(1)[:-1] + "'" + m.group(1)[-1], text)

    # Handle possessives (e.g., "Cats toy" -> "Cat's toy")
    # text = re.sub(r'\b(\w+)s\b(?=\s+\w+)', r"\1's", text)

    text = text.replace("Ive", "I've")
    text = text.replace("v'e", "'ve")
    text = text.replace("our'e", "ou're")
    text = text.replace("Il'l", "I'll")
    text = text.replace("weve", "we've")
    text = text.replace("isnt", "isn't")

    return text


genqus_df = pd.read_csv(genqus_path+".csv")
genqus_df = genqus_df[genqus_df['Type'] == "Emojis"]
genqus_df['Output'] = genqus_df['Output'].apply(replace_apostrophes)

genqus_df.to_csv(genqus_path+"_fixed.csv", index=False)
