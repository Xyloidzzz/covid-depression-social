# correlation between googleTrendsCovidValue and cdcValue in path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

path = "./data/cdcAnxiety_googleCovid_COMBINED.csv"
missingPath = "./data/cdcAnxiety_googleCovid_COMBINED_withMissing.csv"
cdcOGPath = "./data/cdc/cdc_US_anxiety_clean.csv"

# import csv
data = pd.read_csv(path)
missingData = pd.read_csv(missingPath)
cdcData = pd.read_csv(cdcOGPath)

# turn data from string to float
data["cdcValue"] = data["cdcValue"].astype(float)
data["googleTrendsCovidValue"] = data["googleTrendsCovidValue"].astype(float)

# normalize cdcValue and googleTrendsCovidValue
data["cdcValue"] = (data["cdcValue"] - data["cdcValue"].min()) / \
    (data["cdcValue"].max() - data["cdcValue"].min())
data["googleTrendsCovidValue"] = (data["googleTrendsCovidValue"] - data["googleTrendsCovidValue"].min()) / \
    (data["googleTrendsCovidValue"].max() -
     data["googleTrendsCovidValue"].min())

# get correlation between googleTrendsCovidValue and cdcValue
corr = data.corr(method="pearson")
print(corr["cdcValue"]["googleTrendsCovidValue"])

# t-test on googleTrendsCovidValue and cdcValue
t, p = ttest_ind(data["cdcValue"], data["googleTrendsCovidValue"])
print(t, p)

# plot line graph of googleTrendsCovidValue over time
plt.figure(figsize=(20, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Google Trends Value Over Time (After Covid US Start)", fontsize=20)
plt.xlabel("Time", fontsize=16)
plt.ylabel("Google Trends", fontsize=16)
plt.plot(data["week"], data["googleTrendsCovidValue"])
plt.xticks(rotation=90)
plt.show()

# plot line graph of googleTrendsCovidValue over time from OG google data
plt.figure(figsize=(20, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Google Trends Value Over Time (Before Covid US Start)", fontsize=20)
plt.xlabel("Time", fontsize=16)
plt.ylabel("Google Trends", fontsize=16)
plt.plot(missingData["week"], missingData["googleTrendsCovidValue"])
plt.xticks(rotation=90)
plt.show()

# plot line graph of cdcData over time from OG cdc data
plt.figure(figsize=(20, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("CDC Value Over Time (Missing Lockdown)", fontsize=20)
plt.xlabel("Time", fontsize=16)
plt.ylabel("CDC Value", fontsize=16)
plt.plot(cdcData["Time Period"], cdcData["Value"])
plt.show()

# plot the correlation on a scatter graph
# cdcValue on x-axis and googleTrendsCovidValue on y-axis
plt.figure(figsize=(20, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel("CDC", fontsize=16)
plt.ylabel("Google Trends", fontsize=16)
plt.scatter(data["cdcValue"], data["googleTrendsCovidValue"])
z = np.polyfit(data["cdcValue"], data["googleTrendsCovidValue"], 1)
p = np.poly1d(z)
plt.plot(data["cdcValue"], p(data["cdcValue"]), "r-o", markersize=0)
plt.show()

# plot the correlation on a line graph over time
# time on x-axis
# cdcValue on y-axis on the left and googleTrendsCovidValue on y-axis on the right
plt.figure(figsize=(20, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.plot(data["week"], data["cdcValue"], label="CDC")
plt.plot(data["week"], data["googleTrendsCovidValue"], label="Google Trends")
plt.xticks(rotation=90)
plt.legend()
plt.show()
