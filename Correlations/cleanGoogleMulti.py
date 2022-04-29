import os
import pandas as pd

original = "./data/google/original/"

tempPath = "./data/google/temp.csv"

cleanPath = "./data/google/google_trends_CLEAN.csv"

data = pd.DataFrame()

count = 0
# iterate through every file in the original folder
for file in os.listdir(original):
    # open origin file
    with open(original+file, "r") as f:

        # read the file
        read = f.read()
        # split the file into lines
        lines = read.split("\n")

        # remove the first 2 lines
        lines = lines[2:]

        # change the covid: (United States) to covid
        for i in range(len(lines)):
            lines[i] = lines[i].replace(": (United States)", "")
            lines[i] = lines[i].replace("Week", "week")
            lines[i] = lines[i].replace("<1", "1")

        # join the lines back together into one string and make a temporary dataframe
        with open(tempPath, "w") as f:
            f.write("\n".join(lines))

        temp = pd.read_csv(tempPath)
        name = file.split("_")[2].split(".")[0]

        if count == 0:  # if count is 0 then set the dataframe to the temp dataframe
            data = temp
            count += 2
        else:  # if count is not 0 then only append the second column of temp to data
            data[name] = temp.iloc[:, 1]
            count += 1

# save data to cleanPath
data.to_csv(cleanPath, index=False)
print("done")
