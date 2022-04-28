# clean up google trends data

# original = "./data/google/google_trends_covid.csv"
original = "./data/google/google_trends_anxiety.csv"

# cleanPath = "./data/google/google_trends_covid_CLEAN.csv"
cleanPath = "./data/google/google_trends_anxiety_CLEAN.csv"

# open origin file
with open(original, "r") as f:
    # read the file
    data = f.read()
    # split the file into lines
    lines = data.split("\n")
    # remove the first 2 lines
    lines = lines[2:]
    # change the covid: (United States) to covid
    for i in range(len(lines)):
        lines[i] = lines[i].replace(": (United States)", "")
        lines[i] = lines[i].replace("Week", "week")
        lines[i] = lines[i].replace("<1", "1")
    # write to new file
    with open(cleanPath, "w") as f:
        # write the lines to the file
        f.write("\n".join(lines))
