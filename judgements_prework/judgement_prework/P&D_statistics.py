# coding=utf-8
import json

'''
需求如下：
根据json，对于不同的纠纷类型，统计以下信息：
1，原告个数的概率——质量分布图
2，被告个数的概率——质量分布图，以及是否有公司出现，如有，则还需提取公司的经营范围

公司和自然人出现的情况这样定义：
(纠纷类型,a个自然人原告，b个组织原告，c个自然人被告，d个组织被告)：case数量

json需要进行数据清洗：
1，原告必须包含有自然人，通过字符串长度进行分析
2，

'''

def calculate_type(members):
    sum_people = 0
    sum_organization = 0
    for member in members:
        if len(member)<=4:
            sum_people += 1
        else:
            sum_organization += 1
    return sum_people, sum_organization

act_sum = {}
answer = {}
#claims = {}

def inc_element(case_type, a, b, c, d):
    if not case_type in act_sum:
        act_sum[case_type] = 0
    act_sum[case_type] += 1

    if not case_type in answer:
        answer[case_type]= {}
    if not (a,b,c,d) in answer[case_type]:
        answer[case_type][(a, b, c, d)] = 1
    else:
        answer[case_type][(a, b, c, d)] += 1


def solve_json(data):
    plaintiff = data.get('plaintiff', [])
    defendant = data.get('defendant', [])
    case_type = data['case_type']
    claim = data['claim']

    if any(len(s)<=4 for s in plaintiff) and case_type =='劳动争议':
        with open('../files/劳动争议.json','a', errors='ignore', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write('\n')


law_set = set()

f = open('../files/law_use_劳动争议.txt','w', encoding='utf-8')

case_sum = {}

def check_keywords(claim):
    keywords = ['诉讼费', '讼费', '受理费','偿还', '返还', '本金',  '借款', '欠款', '利息', '罚息', '滞纳金', '保全费', '保全', '律师费', '律师服务费', '律师代理费', '违约金', '公告费', '手续费', '鉴定费', '保险费', '赔偿金',
                '连带', '一般保证', '担保', '优先受偿','优先偿还', '解除'
                ]
    for keyword in keywords:
        if claim.find(keyword) != -1:
            return False

    return True

def get_claim(data):
    global case_sum
    plaintiff = data.get('plaintiff', [])
    defendant = data.get('defendant', [])
    case_type = data['case_type']
    claims = data['claim']
    laws = data['laws']

    if any(len(s)<=4 for s in plaintiff):
        if case_type != '劳动争议':
            return
        #if case_type not in case_sum:
        #    case_sum[case_type] = 0
        #case_sum[case_type] += 1
        for law in laws:
            f.write(law)
            f.write('\n')
        #for law in laws:
        #    if law.find('》') != -1:
        #        law_set.add(law)
        #for claim in claims:
        #    if check_keywords(claim):
        #        print(claim)



def extract_and_filter_companies(jsonl_file):
    filtered_companies = []
    with open(jsonl_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            data = json.loads(line)
            solve_json(data)
            get_claim(data)



extract_and_filter_companies('../files/entity_extraction.jsonl')

#with open('../files/case_type_statistic.json','w',encoding='utf-8',errors='ignore') as f:
#    f.write(json.dumps(case_sum,ensure_ascii=False))

for law in law_set:
    print(law)

for key, values in answer.items():
    print(key, ':', act_sum[key])
    for subkey, value in values.items():
        print(key, subkey, value)

