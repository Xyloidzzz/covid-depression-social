import pandas as pd
from datetime import datetime

cdcPath = "./data/cdc/cdcUS.csv"

googleTrendsPath = "./data/google/googleTrendsClean.csv"

combinedPath = "./data/cdcGoogleTrendsCombined.csv"


def dateToList(date, isGoogle):
    """
    Function that takes a date string dd/mm/yyyy and returns it in a list of ints [yyyy, mm, dd]
    """
    if "/" in date:
        date = date.split("/")
    elif "-" in date:
        date = date.split("-")

    if isGoogle:
        return [int(date[0]), int(date[1]), int(date[2])]
    else:
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
    # DataFrame of cdc and google trends data
    cdcData = pd.read_csv(cdcPath)
    googleTrendsData = pd.read_csv(googleTrendsPath)

    # take googleTrendsData week coulumn and make sure its within the cdc data Time Period Start and End columns
    # if they are within, take the cdc data column value of that range and add it to a new googleTrendsData column
    # if not, skip it
    cdcValue = []
    for i in range(len(googleTrendsData)):
        for j in range(len(cdcData)):
            # check if the week is within the cdc data Time Period Start and End columns
            if isBetween(dateToList(googleTrendsData["week"][i], True), dateToList(cdcData["Time Period Start Date"][j], False), dateToList(cdcData["Time Period End Date"][j], False)):
                # if it is, take the cdc data column value of that range and add it to a new googleTrendsData column
                cdcValue.append(cdcData["Value"][j])
                break
            else:
                continue
        if len(cdcValue) == i:
            cdcValue.append("x")

    # add new column
    googleTrendsData["cdcValue"] = cdcValue

    # delete the rows with "x" in the googleTrendsData cdcValue column
    googleTrendsData = googleTrendsData[googleTrendsData["cdcValue"] != "x"]

    # change the depression column label to "googleTrendsValue"
    googleTrendsData = googleTrendsData.rename(
        columns={"depression": "googleTrendsValue"})

    # write the googleTrendsData to a csv
    googleTrendsData.to_csv(combinedPath, index=False)
