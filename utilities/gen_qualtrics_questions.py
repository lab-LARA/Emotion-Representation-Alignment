import os
import itertools
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

"""
THIS SCRIPT CONVERTS THE CSV FILE OF QUESTIONS INTO A FORMAT THAT CAN BE IMPORTED INTO QUALTRICS.

BEFORE RUNNING:
1. CHANGE genqus_path TO THE PATH OF THE QUESTIONS CSV FILE.
2. CHANGE output_directory TO THE PATH TO SAVE THE FORMATTED TEXT FILE

THE ACTUAL SETS OF KEYWORDS USED FOR EACH REPRESENTATION ARE AS FOLLOWS:

for mcqs
words [keywords[0], keywords[1]]
vad [keywords[1], keywords[2]]
vad num [keywords[2], keywords[3]]
emo [keywords[3], keywords[4]]

for sliders
words [keywords[2], keywords[3]]
vad [keywords[3], keywords[4]]
vad num [keywords[4], keywords[0]]
emo [keywords[0], keywords[1]]
"""

genqus_path = os.path.join("..", "data", "generated_questions_llama_3_70B_v4.csv")
output_directory = os.path.join("..", "data", "questions_data", "qualtrics_import_format_llama3")


def build_string_for_survey_emoonly(emo_input: str, options: [str]) -> str:
    tmpl = f"[[Question:MC:List]]\n{emo_input}\n[[Choices]]\n{options[0]}\n{options[1]}\n{options[2]}\n{options[3]}\n\n\n"
    return tmpl

def build_string_for_survey_vadonly(emo_input: str, options: [str]) -> str:
    tmpl = f"[[Question:MC:List]]\n{emo_input}\n[[Choices]]\n{options[0]}\n{options[1]}\n{options[2]}\n{options[3]}\n\n\n"
    return tmpl

def build_string_for_survey_vadnumonly(emo_input: str, options: [str]) -> str:
    vadvals = emo_input.split(",")
    tmpl = f"[[Question:MC:List]]\nValence: {vadvals[0]}, Arousal: {vadvals[1]}, Dominance: {vadvals[2]}\n[[Choices]]\n{options[0]}\n{options[1]}\n{options[2]}\n{options[3]}\n\n\n"
    return tmpl

emo_map = {
    "grateful": "Very High Valence, Moderate Arousal, Low Dominance",
    "joyful": "Very High Valence, High Arousal, High Dominance",
    "content": "Very High Valence, High Arousal, Very High Dominance",
    "surprised": "High Valence, Very High Arousal, Moderate Dominance",
    "excited": "Very High Valence, Very High Arousal, High Dominance",
    "impressed": "High Valence, High Arousal, Low Dominance",
    "proud": "Very High Valence, High Arousal, Very High Dominance",
    "anxious": "Moderate Valence, High Arousal, Moderate Dominance",
    "afraid": "Very Low Valence, Very High Arousal, Low Dominance",
    "terrified": "Very Low Valence, Very High Arousal, Low Dominance",
    "annoyed": "Low Valence, Moderate Arousal, Moderate Dominance",
    "angry": "Low Valence, High Arousal, High Dominance",
    "furious": "Low Valence, Very High Arousal, High Dominance",
    "sad": "Very Low Valence, Low Arousal, Low Dominance",
    "devastated": "Moderate Valence, High Arousal, Low Dominance",
    "ashamed": "Low Valence, Mid Arousal, Low Dominance",
    "embarrassed": "Low Valence, High Arousal, Low Dominance",
    "guilty": "Low Valence, High Arousal, Low Dominance"
}

num_map = {
    "grateful": "2.5,0.0,-2.5",
    "joyful": "4.0,1.0,1.0",
    "content": "4.0,0.0,4.0",
    "surprised": "1.0,2.5,-2.5",
    "excited": "2.5,4.0,1.0",
    "impressed": "1.0,1.0,-4.0",
    "proud": "4.0,1.0,2.5",
    "anxious": "-1.0,2.5,-2.5",
    "afraid": "-5.0,2.5,-4.0",
    "terrified": "-5.0,4.0,-4.0",
    "annoyed": "-2.5,0.0,-1.0",
    "angry": "-5.0,2.5,0.0",
    "furious": "-4.0,4.0,1.0",
    "sad": "-4.0,-2.5,-4.0",
    "devastated": "-5.0,1.0,-2.5",
    "ashamed": "-3.0,-1.0,-4.0",
    "embarrassed": "-4.0,2.5,-2.5",
    "guilty": "-4.0,0.0,-4.0"
}

genqus_df = pd.read_csv(genqus_path)
genqus_df_sorted = genqus_df.sort_values(by=['Keywords', 'Emotion'], ascending=True)

# emotions = genqus_df_sorted['Emotion'].unique().tolist()
emotions_lst = list(emo_map.keys())
keywords = genqus_df_sorted['Keywords'].unique().tolist()


with open(os.path.join(output_directory, 'tsftxt_sep_repr_words.txt'), 'a', encoding="utf-8") as file:

    for em, kw in itertools.product(emotions_lst, [keywords[0], keywords[1]]):
        genqus_df_curr = genqus_df_sorted[(genqus_df_sorted['Emotion'] == em) & (genqus_df_sorted['Keywords'] == kw)]
        op = build_string_for_survey_emoonly(emo_input=em.capitalize(), options=genqus_df_curr['Output'].tolist())
        file.write(op)

with open('../data/questions_data/qualtrics_import_format_2/tsftxt_sep_repr_vad.txt', 'a', encoding="utf-8") as file:

    for em, kw in itertools.product(emotions_lst, [keywords[1], keywords[2]]):
        genqus_df_curr = genqus_df_sorted[(genqus_df_sorted['Emotion'] == em) & (genqus_df_sorted['Keywords'] == kw)]
        op = build_string_for_survey_vadonly(emo_input=emo_map.get(em), options=genqus_df_curr['Output'].tolist())
        file.write(op)

with open('../data/questions_data/qualtrics_import_format_2/tsftxt_sep_repr_vadnum.txt', 'a', encoding="utf-8") as file:

    for em, kw in itertools.product(emotions_lst, [keywords[2], keywords[3]]):
        genqus_df_curr = genqus_df_sorted[(genqus_df_sorted['Emotion'] == em) & (genqus_df_sorted['Keywords'] == kw)]
        op = build_string_for_survey_vadnumonly(emo_input=num_map.get(em), options=genqus_df_curr['Output'].tolist())
        file.write(op)

with open('../data/questions_data/qualtrics_import_format_2/tsftxt_sep_repr_emoji.txt', 'a', encoding="utf-8") as file:

    for em, kw in itertools.product(emotions_lst, [keywords[3], keywords[4]]):
        genqus_df_curr = genqus_df_sorted[(genqus_df_sorted['Emotion'] == em) & (genqus_df_sorted['Keywords'] == kw)]
        op = build_string_for_survey_emoonly(emo_input=genqus_df_curr['Emoji'].unique().tolist()[-1], options=genqus_df_curr['Output'].tolist())
        file.write(op)