import ast
import jieba
keyword = []

with open('../files/词频统计(民间借贷纠纷清洗版).txt','r',encoding='utf-8') as f:
    for line in f:
        tuple = ast.literal_eval(line)
        keyword.append(tuple[0])

while True:
    text = input('输入诉讼请求:')
    lst = jieba.lcut(text)
    for word in lst:
        if word in keyword:
            print(word, end='')
    print()
