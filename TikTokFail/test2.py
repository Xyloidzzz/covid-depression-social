import ijson

# file path
path = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok-sample.json"


# def extract_json(filename):
#     with open(filename, 'r') as input_file:
#         return list(ijson.items(input_file, 'items', multiple_values=True))

def extract_json(filename):
    with open(filename, 'r') as input_file:
        return list(ijson.kvitems(input_file, ''))


# main
if __name__ == "__main__":
    data = extract_json(path)
    print(data)
