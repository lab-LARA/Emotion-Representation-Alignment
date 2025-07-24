import os
import time
import torch
import pandas as pd
from pprint import pprint

from run_infer import main

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

"""
THIS SCRIPT GENERATES A LIST OF SENTENCES FOR QUESTIONS IN CSV FORMAT, BASED ON A LIST OF KEYWORDS AND EMOTIONS AS GIVEN IN THE QUESTIONS DATA FILE.

FOR EACH ROW IN THE QUESTIONS DATA FILE, IT CHECKS THE REPRESENTATION, EMOTION AND KEYWORDS, THEN USES main FROM run_infer.py TO GENERATE THE SENTENCE.

IMPORTANT: UPDATE ALL FOUR task VARIABLES WHEN CHANGING THE MODEL.
"""

questions_data_path = os.path.join("data", "questions_data", "set_1", "emoquestions_data_rescaled.csv")
save_generated_data = os.path.join("data", "generated_questions_llama_3_8B.csv")

questions_df = pd.read_csv(questions_data_path).sample(n=10, random_state=0)

for _, row in questions_df.iterrows():

    emo = None

    if row.Type == "Emotion":
        emo = row.Emotion
        task = "llama_3_conversation"       # UPDATE THIS WHEN CHANGING MODEL
        questions_df.at[_, "Output"], questions_df.at[_, "Full_Prompt"] = main(task=task, emo=emo, v=None, a=None, d=None, keywords=row.Keywords)

    if row.Type == "Emojis":
        emo = row.Emoji
        task = "llama_3_conversation"       # UPDATE THIS WHEN CHANGING MODEL
        questions_df.at[_, "Output"], questions_df.at[_, "Full_Prompt"] = main(task=task, emo=emo, v=None, a=None, d=None, keywords=row.Keywords)

    if row.Type == "VAD":
        v, a, d = row.Valence, row.Arousal, row.Dominance
        task = "llama_3_conversation_vad"    # UPDATE THIS WHEN CHANGING MODEL
        questions_df.at[_, "Output"], questions_df.at[_, "Full_Prompt"] = main(task=task, emo=emo, v=v, a=a, d=d, keywords=row.Keywords)

    if row.Type == "VAD_Numeric":
        v, a, d = row.V, row.A, row.D
        task = "llama_3_conversation_vad"    # UPDATE THIS WHEN CHANGING MODEL
        questions_df.at[_, "Output"], questions_df.at[_, "Full_Prompt"] = main(task=task, emo=emo, v=v, a=a, d=d, keywords=row.Keywords)

    print(questions_df.at[_, "Full_Prompt"], questions_df.at[_, "Output"])


questions_df.to_csv(save_generated_data)



