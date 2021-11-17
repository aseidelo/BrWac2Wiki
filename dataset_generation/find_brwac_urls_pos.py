from codecs import open
import pandas as pd
import json
from os import listdir
from os.path import isfile, join

input_path = 'data/brwac_ref_urls_sentences_v4/'
urls = []
files = []
pos = []
file_names = [f for f in listdir(input_path) if isfile(join(input_path, f)) and 'serialized' not in f]
j = 0
for file_name in file_names:
    i = 0
    print('({}/{}) {}'.format(j, len(file_names), file_name))
    with open(join(input_path, file_name), 'r') as f:
        for line in f:
            content = json.loads(line)
            urls.append(content['docid'])
            files.append(file_name)
            pos.append(i)
            i = i + 1
    j = j + 1
df = pd.DataFrame({'docid' : urls, 'file' : files, 'pos' : pos})
df.to_csv(input_path + 'urls_pos.csv', index=False)
