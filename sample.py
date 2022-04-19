import ijson
from tqdm import tqdm

# file path
path = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok.json"

# open the json file with ijson
with open(path, "r") as f:
    # read the json file with ijson
    print("before data")
    data = ijson.items(f, "item", multiple_values=True)
    # data = (o for o in objects)
    print(data)
    print("after data")
    # # take the first 100 items
    # data = list(data)[:100]
    count = 0
    # iterate over data and count the number of times the hashtag appears
    print("before loop")
    for item in tqdm(data):
        print("during loop")
        # check if the hashtag is in the item
        if "textExtra" in item:
            # check if the hashtag is depression
            for extra in item["textExtra"]:
                if "depression" in extra["hashtagName"]:
                    # if it is, increase the counter
                    count += 1
    print("after loop")
    print(count)
