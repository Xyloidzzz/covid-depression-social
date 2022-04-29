import re
import pandas as pd

original = "./data/cdc/Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv"

seperate = "./data/cdc/seperate-anxiety/"

allPath = "./data/cdc/CDCAnxiety_CLEAN.csv"

names = ["National Estimate", "By Age", "By Sex",
         "By Race", "By Education", "By State"]

df = pd.read_csv(original)

# delete last 4 columns
df = df.drop(df.columns[-4:], axis=1)

# check Indicator and keep only "Symptoms of Anxiety Disorder"
df = df[df["Indicator"] == "Symptoms of Anxiety Disorder"]

# delete the rows with Phase of -1
df = df[df["Phase"] != "-1"]

# Phase column remove strings within parentheses but keep the numbers or floats within that cell
df = df.replace(r"\(.*\)", "", regex=True)

# loop through all the names
for name in names:
    temp = df[df["Group"] == name]
    temp.to_csv(seperate+"CDCAnxiety_" +
                re.sub(r"\s+", "", name)+".csv", index=False)
