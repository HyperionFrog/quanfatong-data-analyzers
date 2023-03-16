import jieba
from collections import Counter

words_sum = []

with open('../company.txt', 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        words = list(jieba.cut(line))
        print(words)
        words_sum += words

statistic = Counter(words_sum)
print(statistic)