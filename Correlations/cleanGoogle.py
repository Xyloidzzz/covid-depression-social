# clean up google trends data

original = "./data/google/multiTimeline.csv"

cleanPath = "./data/google/googleTrendsClean.csv"

# open origin file
with open(original, "r") as f:
    # read the file
    data = f.read()
    # split the file into lines
    lines = data.split("\n")
    # remove the first 2 lines
    lines = lines[2:]
    # change the depression: (United States) to depression
    for i in range(len(lines)):
        lines[i] = lines[i].replace(": (United States)", "")
        lines[i] = lines[i].replace("Week", "week")
    # write to new file
    with open(cleanPath, "w") as f:
        # write the lines to the file
        f.write("\n".join(lines))
