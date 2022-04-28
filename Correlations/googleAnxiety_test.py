import pandas as pd

path = "./data/google/google_trends_anxiety_CLEAN.csv"

df = pd.read_csv(path)

print(df["anxiety"].min(), df["anxiety"].max(), df["anxiety"].mean())
