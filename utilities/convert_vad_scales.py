import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

"""
THIS SCRIPT WAS USED TO NORMALIZE THE V-A-D VALUES TO A RANGE OF -5 TO +5

YOU PROBABLY WON'T NEED THIS UNLESS YOU INITIALLY START WITH VAD VALUES IN A DIFFERENT RANGE.
OR NEED TO CHANGE IT TO YET ANOTHER RANGE.

BEFORE RUNNING, CHANGE DATA_PATH TO THE LOCATION OF THE QUESTIONS FILE TO CHANGE.
"""

data_path = os.path.join("..", "data", "questions_data", "set_1", "emoquestions_data")
data_df = pd.read_csv(data_path+".csv")

# print(data_df.head(50))

def convert_range(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

# Convert values in the range 1 to 4 to the range -5 to 5
old_min, old_max = 1, 5
new_min, new_max = -5, 5

for _, row in data_df.iterrows():

    if row.Type == "VAD_Numeric":
        data_df.at[_, "V"] = round(convert_range(row.V, old_min, old_max, new_min, new_max) * 2) / 2
        data_df.at[_, "A"] = round(convert_range(row.A, old_min, old_max, new_min, new_max) * 2) / 2
        data_df.at[_, "D"] = round(convert_range(row.D, old_min, old_max, new_min, new_max) * 2) / 2

data_df.to_csv(data_path+"_rescaled.csv", index=False)

