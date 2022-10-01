data = []

import json
import pandas as pd

df = pd.read_csv("data/Data/udemy/keywords.txt")
keywords = df["0"].tolist()


for i in range(len(keywords)):
    for line in open('data/Data/udemy/udemy_info_{}.json'.format(i), 'r'):
        data.append(json.loads(line))

df = pd.DataFrame(data)
df.to_json('data/data.json', orient='records', lines=True)