# take the json from "G:\xyloid\dev\Data\tiktok\tiktok-2020_07-10" and check for the hashtag # depression and count how many times it appears


import json
import ijson
from tqdm import tqdm
import os
import re
import sys
import time

import pandas as pd

# from tqdm import tqdm

# file path
path = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok-sample.json"

# open the json file with ijson
with open(path, "r") as f:
    # read the json file with ijson
    data = ijson.items(f, "item", multiple_values=True)
    # # take the first 100 items
    # data = list(data)[:100]
    count = 0
    # iterate over data and count the number of times the hashtag appears
    for item in tqdm(data):
        # check if the hashtag is in the item
        if "hashtagName" in item:
            # check if the hashtag is depression
            if "depression" in item["hashtagName"]:
                # if it is, increase the counter
                count += 1

    # # count how many times it appears
    # count = 0
    # for item in videos:
    #     print(count)
    #     if item["desc"] == "#boredinthehouse":
    #         count += 1
    #         print(count)
