import json
import re
import sys
from tqdm import tqdm

import jieba

class make_graph:
    mp = {}
    word_mp = {}

    def add_edge(self, str1, str2):
        if str1 not in self.mp:
            self.mp[str1] = {}

        if str2 not in self.mp[str1]:
            self.mp[str1][str2] = 0

        self.mp[str1][str2] += 1

    def add_word(self, text, type):
        if text not in self.word_mp:
            self.word_mp[text] = {}

        if type not in self.word_mp[text]:
            self.word_mp[text][type] = 0
        self.word_mp[text][type] += 1


    def __init__(self, filepath):
        def legal_check(text):
            if re.search(r'\d', text):
                return False
            punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
                            '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '！', '“', '”', '#',
                            '￥', '%', '&', '‘', '’', '（', '）', '*', '+', '，', '-', '。', '、', '：', '；', '《', '》', '？',
                            '@', '【', '】', '^', '_', '‘', '’', '｛', '｜', '｝', '~']

            if any(s in text for s in punctuations):
                return False
            return True

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for all, line in enumerate(f):
                pass
            all_data = range(all)

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i in tqdm(all_data, desc='Processing data'):
                text = f.readline()
                try:
                    data = json.loads(text)
                except:
                    break

                #if data['case_type'] != '民间借贷纠纷':
                #    continue
                plaintiff = data['plaintiff']
                type = data['case_type']
                claims = data['claim']

                if not any(len(s)<=4 for s in plaintiff):
                    continue

                for claim in claims:
                    words = jieba.lcut(claim)

                    new_words = []
                    for word in words:
                        if legal_check(word):
                            new_words.append(word)
                    words = new_words

                    for i, word1 in enumerate(words):
                        self.add_word(word1, type)

                        #continue
                        for j, word2 in enumerate(words):
                            if i!=j:
                                self.add_edge(word1, word2)

    def print_node(self,node_name):
        sorted_dict = sorted(self.mp[node_name].items(), key=lambda x: x[1], reverse=False)
        for key, value in sorted_dict:
            print(key, value)

    def print_word(self):
        sorted_dict = sorted(self.word_mp.items(), key=lambda x: sum(x[1].values()), reverse=False)
        with open("../files/keywords_extraction.jsonl", "w", encoding="utf-8") as f:
            for key, value in sorted_dict:
                new_dict = sorted(value.items(), key=lambda x: x[1], reverse=True)
                print(key, new_dict, sep=' ')
                data = {
                    'key': key,
                    'type': [x[0] for x in new_dict],
                    'sum': [x[1] for x in new_dict]
                }
                f.write(json.dumps(data, ensure_ascii=False))
                f.write("\n")


a = make_graph('../files/entity_extraction.jsonl')
with open('../files/graph.txt','w',encoding='utf-8') as f:
    text = json.dumps(a.mp, ensure_ascii=False)
    f.write(text)

print('finished')
while True:
    word = input('input your word:')
    a.print_node(word)