import pandas as pd
import json, jieba
from tqdm import tqdm

with open("output2.json", "r", encoding="utf-8") as file:
    judgements = json.loads(file.read())
    file.close()


word_to_frequency = {}


def count(word):
    global word_to_frequency
    if word in word_to_frequency:
        word_to_frequency[word] += 1
    else:
        word_to_frequency[word] = 1


for judgement in tqdm(judgements):
    words = jieba.lcut(judgement["article"])
    for word in words:
        count(word)

word_to_frequency = {k: v for k, v in sorted(word_to_frequency.items(), key=lambda x: x[1], reverse=True)}

with open("word_frequency.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(word_to_frequency, ensure_ascii=False, indent='\t'))
    file.close()