# correlation between googleTrendsValue and cdcValue in path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

path = "./data/cdcGoogleTrendsCombined.csv"
missingPath = "./data/cdcGoogleTrendsCombined_withMissing.csv"
cdcOGPath = "./data/cdc/cdcUS.csv"

# import csv
data = pd.read_csv(path)
missingData = pd.read_csv(missingPath)
cdcData = pd.read_csv(cdcOGPath)

# turn data from string to float
data["cdcValue"] = data["cdcValue"].astype(float)
data["googleTrendsValue"] = data["googleTrendsValue"].astype(float)

# normalize cdcValue and googleTrendsValue
data["cdcValue"] = (data["cdcValue"] - data["cdcValue"].min()) / \
    (data["cdcValue"].max() - data["cdcValue"].min())
data["googleTrendsValue"] = (data["googleTrendsValue"] - data["googleTrendsValue"].min()) / \
    (data["googleTrendsValue"].max() - data["googleTrendsValue"].min())

# get correlation between googleTrendsValue and cdcValue
corr = data.corr(method="pearson")
print(corr["cdcValue"]["googleTrendsValue"])

# t-test on googleTrendsValue and cdcValue
t, p = ttest_ind(data["cdcValue"], data["googleTrendsValue"])
print(t, p)

# # plot line graph of googleTrendsValue over time
# plt.figure(figsize=(20, 10))
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.title("Google Trends Value Over Time (After Covid US Start)", fontsize=20)
# plt.xlabel("Time", fontsize=16)
# plt.ylabel("Google Trends", fontsize=16)
# plt.plot(data["week"], data["googleTrendsValue"])
# plt.xticks(rotation=90)
# plt.show()

# # plot line graph of googleTrendsValue over time from OG google data
# plt.figure(figsize=(20, 10))
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.title("Google Trends Value Over Time (Before Covid US Start)", fontsize=20)
# plt.xlabel("Time", fontsize=16)
# plt.ylabel("Google Trends", fontsize=16)
# plt.plot(missingData["week"], missingData["googleTrendsValue"])
# plt.xticks(rotation=90)
# plt.show()

# plot line graph of cdcData over time from OG cdc data
plt.figure(figsize=(20, 10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("CDC Value Over Time (Missing Lockdown)", fontsize=20)
plt.xlabel("Time", fontsize=16)
plt.ylabel("CDC Value", fontsize=16)
plt.plot(cdcData["Time Period"], cdcData["Value"])
plt.show()

# # plot the correlation on a scatter graph
# # cdcValue on x-axis and googleTrendsValue on y-axis
# plt.figure(figsize=(20, 10))
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.xlabel("CDC", fontsize=16)
# plt.ylabel("Google Trends", fontsize=16)
# plt.scatter(data["cdcValue"], data["googleTrendsValue"])
# z = np.polyfit(data["cdcValue"], data["googleTrendsValue"], 1)
# p = np.poly1d(z)
# plt.plot(data["cdcValue"], p(data["cdcValue"]), "r-o", markersize=0)
# plt.show()

# # plot the correlation on a line graph over time
# # time on x-axis
# # cdcValue on y-axis on the left and googleTrendsValue on y-axis on the right
# plt.figure(figsize=(20, 10))
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.plot(data["week"], data["cdcValue"], label="CDC")
# plt.plot(data["week"], data["googleTrendsValue"], label="Google Trends")
# plt.xticks(rotation=90)
# plt.legend()
# plt.show()
