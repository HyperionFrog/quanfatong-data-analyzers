import json

with open('../files/case_type_statistic.json','r',encoding='utf-8', errors='ignore') as f:
    case_info = json.load(f)
    #for key,value in case_info.items():
    #    case_info[key] = int(value)

keywords = []
with open('../files/keywords_extraction.jsonl','r',encoding='utf-8', errors='ignore') as f:
    for line in f:
        a = json.loads(line)
        keywords.append(a)

def calc():
    key_type = input('输入纠纷类型')
    percent_base = case_info[key_type]/sum(x for x in case_info.values())
    print(percent_base)
    answer = []
    for keyword in keywords:
        try:
            id = keyword['type'].index(key_type)
        except:
            continue

        keyword_all = sum(keyword['sum'])
        if keyword_all <100:
            continue

        percent_now = keyword['sum'][id]/keyword_all
        if percent_now>percent_base:
            answer.append((keyword['key'],keyword_all*pow(percent_now/percent_base -1, 2), keyword_all, percent_now/percent_base))
            #print(keyword['key'])

    answer = sorted(answer, key=lambda x: x[1], reverse=False)
    #print(answer)
    for ans in answer:
        print(ans)

while True:
    calc()