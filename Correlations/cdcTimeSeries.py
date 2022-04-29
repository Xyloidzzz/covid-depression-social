import re
import pandas as pd
import numpy as np
from datetime import datetime

whatVersion = "seperate-anxiety"

cdcPath = "./data/cdc/"+whatVersion+"/"

googleTrendsPath = "./data/google/google_trends_CLEAN.csv"

timePath = "./data/cdc/"+whatVersion+"/time-series/"  # CDCAnxiety_TIMESERIES.csv

names = ["National Estimate", "By Age", "By Sex",
         "By Race", "By Education", "By State"]


def dateToList(date):
    """
    Function that takes a date string dd/mm/yyyy and returns it in a list of ints [yyyy, mm, dd]
    """
    if "/" in date:
        date = date.split("/")
    elif "-" in date:
        date = date.split("-")

    return [int(date[2]), int(date[0]), int(date[1])]


def isBetween(date, dateStart, dateEnd):
    """
    Function that takes 3 list of ints [yyyy, mm, dd] and checks if the first one is between the second(start) and third(end)
    """
    if datetime(date[0], date[1], date[2]) >= datetime(dateStart[0], dateStart[1], dateStart[2]) and datetime(date[0], date[1], date[2]) <= datetime(dateEnd[0], dateEnd[1], dateEnd[2]):
        return True
    else:
        return False


# main
if __name__ == '__main__':
    # read the google trends data
    googleTrendsData = pd.read_csv(googleTrendsPath)

    # loop through names
    for name in names:
        # select the file based on name
        cdcData = pd.read_csv(cdcPath+"CDCAnxiety_" +
                              re.sub(r"\s+", "", name)+".csv")

        # get unique subgroups
        subgroupNames = cdcData["Subgroup"].unique()

        # set up temp with week
        temp = pd.DataFrame(googleTrendsData["week"])
        temp.reset_index(inplace=True)
        temp = temp.drop(temp.columns[0], axis=1)

        # loop through subgroups
        for subgroup in subgroupNames:
            # select the data for the subgroup
            subgroupData = pd.DataFrame(cdcData[cdcData["Subgroup"] == subgroup])
            subgroupData.reset_index(inplace=True)
            subgroupData = subgroupData.drop(subgroupData.columns[0], axis=1)
            temp.reset_index(inplace=True)
            temp = temp.drop(temp.columns[0], axis=1)
            cdcValues = []
            for i in range(len(temp)):
                for j in range(len(subgroupData)):
                    # check if the week is within the cdc data Time Period Start and End columns
                    if isBetween(dateToList(temp["week"][i]), dateToList(subgroupData["Time Period Start Date"][j]), dateToList(subgroupData["Time Period End Date"][j])):
                        # if it is, take the cdc data column value of that range and add it to a new googleTrendsData column
                        cdcValues.append(subgroupData["Value"][j])
                        break
                    else:
                        continue
                if len(cdcValues) == i:
                    cdcValues.append("x")

            # add new column
            temp[subgroup] = cdcValues

            # delete the rows with "x" in the temp subgroup column
            temp = temp[temp[subgroup] != "x"]

        # write the temp to a csv
        temp.to_csv(timePath+"CDCAnxiety_" +
                    re.sub(r"\s+", "", name)+"_TIMESERIES.csv", index=False)
