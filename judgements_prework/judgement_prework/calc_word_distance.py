import json

with open('../files/graph.txt','r',encoding='utf-8') as f:
    text = f.readline()
    mp = json.loads(text)

def calc_word_distance(word1, word2):
    if (word1 not in mp) or (word2 not in mp):
        print('err: one of the word is not in the library')
        return

    sum1 = sum(y for x,y in mp[word1].items())
    sum2 = sum(y for x,y in mp[word2].items())
    diff = 0
    sum3 = 0

    for key, value in mp[word1].items():
        percent_1 = value/sum1
        percent_2 = 0

        if key in mp[word2]:
            percent_2 = mp[word2][key]/sum2

        diff += pow(percent_1-percent_2, 2)*(percent_1 + percent_2)
        sum3 += pow(percent_1,3)

    for key, value in mp[word2].items():
        percent_2 = value / sum2
        sum3 += pow(percent_2, 3)

        if key not in mp[word1]:
            diff += pow(percent_2, 3)

    print(diff/sum3)

while True:
    text1, text2 = input('请输入两个词'), input()
    calc_word_distance(text1, text2)