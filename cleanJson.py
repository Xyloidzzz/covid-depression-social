import json
import ijson
import fileinput

path = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok.txt"
newPath = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok-clean.json"

# load json file as string and add [ to the beggining and ] to the end of the file
# then add commas after every object
# finally change string back to json

# read .txt file
with open(path, "r") as f:
    data = f.read()
    data = "[" + data + "]"
    data = data.replace("}", "},\n")

# write to new file
with open(newPath, "w") as g:
    g.write(data)
