# clean cdc data to be US only and remove breaks

import pandas as pd

original = "./data/cdc/Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv"

cleanPath = "./data/cdc/cdc_US_anxiety_clean.csv"


df = pd.read_csv(original)

# delete last 4 columns
df = df.drop(df.columns[-4:], axis=1)

# grab only the National Estimate from the Group column
df = df[df["Group"] == "National Estimate"]

# delete the rows with Phase of -1
df = df[df["Phase"] != "-1"]

# Phase column remove strings within parentheses but keep the numbers or floats within that cell
df = df.replace(r"\(.*\)", "", regex=True)

# check Indicator and keep only "Symptoms of Anxiety Disorder"
df = df[df["Indicator"] == "Symptoms of Anxiety Disorder"]

print(df.head())

# write dataframe to csv (if no file create it)
df.to_csv(cleanPath, index=False)
