import re
import pandas as pd

data_df = pd.read_csv("generated_questions_llama3_70B_vadintegers.csv")

for _, row in data_df.iterrows():
    if row.Type == "VAD_Numeric":
        op = row.Output.split("Now, respond to the following:", 1)[-1].strip()
        op = op.split("Dialogue:", 1)[-1].strip()
        op = op.split("\n", 1)[0].strip()

        keywords = row.Keywords.split(", ")

        op = op.replace("Morring", "Morning").replace("Morring", "Morning")
        if any(keyword.lower() in op.lower() for keyword in keywords):
            data_df.at[_, "Output"] = op
        else:
            data_df.at[_, "Output"] = "MANUAL CHECK" + row.Output

data_df.to_csv("generated_questions_llama3_70B_vadintegers_fixed.csv")
