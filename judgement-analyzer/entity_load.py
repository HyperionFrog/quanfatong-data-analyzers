# Author: AlphaINF

import codecs
import re
import json
from string2laws import string2laws

def load_anyous():
    with open("./assets/anyou.txt", "r", encoding='utf-8') as f:
        data = json.load(f)
    text_list = [d['text'] for d in data]
    return text_list

anyous = load_anyous()


class Judgenemt:
    files = []

    def check_keywords(self, str, keywords):
        start = 0
        for keyword in keywords:
            index = str.find(keyword, start)
            if index == -1:
                return False
            start = index + len(keyword)
        return True

    def select_words(self, str, key1, key2):
        start_idx = str.find(key1) + len(key1)
        if key2 != '':
            end_idx = str.find(key2, start_idx)
        else:
            end_idx = len(str)
        return str[start_idx:end_idx]

    def init_special(self):
        #将诉讼请求与事实和理由合并在一行内
        for i in range(len(self.files)-1):
            if self.check_keywords(self.files[i], ['诉讼请求']) and self.check_keywords(self.files[i+1], ['事实', '理由']):
                self.files[i] = self.files[i] + self.files[i+1]
                self.files.pop(i+1)
                break

        #合并本院认为
        for i in range(len(self.files)-1):
            if self.check_keywords(self.files[i], ['本院认为']):
                if self.check_keywords(self.files[i], ['依', '《', '》', '第', '条', '判决如下']):
                    #需要进行拆分
                    yi_id = self.files[i].rfind('依')
                    new_line = self.files[i][yi_id:]

                    self.files[i] = self.files[i][:yi_id]
                    self.files.insert(i+1, new_line)

                    break

                if self.check_keywords(self.files[i], ['根', '《', '》', '第', '条', '判决如下']):
                    #需要进行拆分
                    yi_id = self.files[i].rfind('根')
                    new_line = self.files[i][yi_id:]

                    self.files[i] = self.files[i][:yi_id]
                    self.files.insert(i+1, new_line)

                    break

                while True:
                    if self.check_keywords(self.files[i+1], ['依', '《', '》', '第', '条', '判决如下']):
                        break
                    if self.check_keywords(self.files[i+1], ['根', '《', '》', '第', '条', '判决如下']):
                        break
                    self.files[i] = self.files[i] + self.files[i+1]
                    self.files.pop(i+1)
                break

        #给原被告加冒号
        for i in range(len(self.files)):
            if self.check_keywords(self.files[i], ['一案']) or self.check_keywords(self.files[i], ['终结']):
                break
            if self.check_keywords(self.files[i], ['原告']) and (not self.check_keywords(self.files[i], ['原告：'])):
                self.files[i] = self.files[i].replace('原告', '原告：')
            if self.check_keywords(self.files[i], ['被告']) and (not self.check_keywords(self.files[i], ['被告：'])):
                self.files[i] = self.files[i].replace('被告', '被告：')

        #一些符号的标准化
        for i in range(len(self.files)):
            self.files[i] = self.files[i].replace(':', '：')
            self.files[i] = self.files[i].replace(',', '，')
            self.files[i] = self.files[i].replace('１', '1')
            self.files[i] = self.files[i].replace('２', '2')
            self.files[i] = self.files[i].replace('３', '3')
            self.files[i] = self.files[i].replace('４', '4')
            self.files[i] = self.files[i].replace('５', '5')
            self.files[i] = self.files[i].replace('６', '6')
            self.files[i] = self.files[i].replace('７', '7')
            self.files[i] = self.files[i].replace('８', '8')
            self.files[i] = self.files[i].replace('９', '9')
            self.files[i] = self.files[i].replace('０', '0')


    def read_text(self, text):
        self.files = text
        try:
            self.init_special()
        except:
            val = 0
            #print("init warning..")

    def __init__(self, text):
        self.read_text(text)

    def get_info(self, keys, key1, key2 = ''):
        answer = []
        for line in self.files:
            if self.check_keywords(line, keys):
                answer.append(self.select_words(line, key1, key2))
        return answer

    def get_member_fixbug(self, element):
        #return element
        for i in range(len(element)):
            if element[i].find('。')!=-1:
                element[i] = element[i][:element[i].find('。')]
            if element[i].find('，')!=-1:
                element[i] = element[i][:element[i].find('，')]
            if element[i].find('、')!=-1:
                element[i] = element[i][:element[i].find('、')]
        return element

    def get_plaintiff(self):
        return self.get_member_fixbug(self.get_info(['原告：'], '原告：'))


    def get_defendant(self):
        return self.get_member_fixbug(self.get_info(['被告：'], '被告：'))

    def get_claim(self):
        try:
            all = self.get_info(['诉讼请求', '事实', '理由'], '诉讼请求：', '事实')[0]
        except:
            all = self.get_info(['诉讼请求'], '诉讼请求：')[0]
        #print(all)

        def find_id(text, num, start = 0):
            split_dots = [',', '，', '.', '，', '．', '、', '.']
            for split_dot in split_dots:
                tag = str(num) + split_dot
                pos = text.find(tag, start)
                if pos != -1:
                    if (not text[pos-1].isdigit()) and (not text[pos+2].isdigit()):
                        return pos
                    else:
                        start = pos + 2
            return -1

        offset = find_id(all, 1)
        answer = []

        if offset == -1:
            answer.append(all)
            return answer

        for require_id in range(2, 10):
            pos = find_id(all, require_id, offset)
            if pos == -1:
                answer.append(all[offset:])
                break
            answer.append(all[offset:pos])
            offset = pos

        return answer

    def get_complaint(self):
        try:
            ret = self.get_info(['诉讼请求', '事实', '理由'], '理由：')[0]
            return ret
        except:
            return ''

    def get_answer(self):
        return self.get_info(['辩称'], '辩称')

    def get_judge(self):
        answer = []
        startkey = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
        for i in range(len(self.files)):
            if self.check_keywords(self.files[i], ['依', '《', '》', '第', '条', '判决如下']):
                for j in range(len(startkey)):
                    if self.files[i+j+1].startswith(startkey[j]):
                        answer.append(self.files[i+j+1])
                    else:
                        break
                if j == 0:
                    answer.append(self.files[i+1])
        return answer

    def get_laws(self):
        try:
            all = '依' + self.get_info(['依', '《', '》', '第', '条', '判决如下'], '依')[0]
        except:
            all = '依' + self.get_info(['根', '《', '》', '第', '条', '判决如下'], '跟')[0]
        idr = all.rfind('判决如下')
        all = all[:idr]
        idr = all.rfind('依')
        all = all[idr:]
        #print(all)
        #print(len(all))

        def remove_prefix(string):
            index = string.find("《")
            if index != -1:
                string = string[index:]
                indexR = max(string.rfind("条"), string.rfind("款"), string.rfind("项"))
                return string[:indexR+1]
            return ''

        laws = all.split('《')

        answer = []
        for law in laws:
            law = '《' + law
            law = remove_prefix(law)
            if law != '':
                answer.append(law)

        output = []
        for law in answer:
            to_law = string2laws(law)
            out = to_law.outall_simple()
            output.extend(out)
        return output

    def get_case_type(self):
        all = self.get_info(['案', '终结'], '', '案')[0]
        answer = ''
        for anyou in anyous:
            if all.find(anyou) != -1:
                if len(answer)<len(anyou):
                    answer = anyou
        return answer

    def get_think(self):
        all = self.get_info(['本院认为'], '本院认为')[0]
        return all[1:]

    def outputJSON(self):
        try:
            plaintiff = self.get_plaintiff() #原告列表
            defendant = self.get_defendant() #被告列表
            case_type = self.get_case_type() #纠纷类型
            claim = self.get_claim() #诉讼请求列表
            complaint = self.get_complaint() #事实与理由
            answer = self.get_answer() #被告答辩列表
            think = self.get_think() #本院认为
            laws = self.get_laws() #适用法律列表
            judge = self.get_judge() #判决结果列表
        except:
            return -1

        if len(plaintiff) == 0 or len(defendant) == 0 or len(case_type) ==0 or len(claim) ==0 :
            return -1

        if len(complaint) == 0 or len(think) == 0 or len(laws) == 0 or len(judge) ==0:
            return -1

        data = {
            "plaintiff" : plaintiff,
            "defendant" : defendant,
            "case_type" : case_type,
            "claim"     : claim,
            "complaint" : complaint,
            "answer"    : answer,
            "think"     : think,
            "laws"      : laws,
            "judge"     : judge
        }

        return data

    # funcs_for_fields = {
    #     "plaintiff": get_plaintiff,
    #     "defendant": get_defendant,
    #     "claim": get_claim
    # }

'''
def solve_txt(txt_fil)


with codecs.open("jsonl_file.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(data, ensure_ascii=False))
    f.write("\n")
'''

#a = Judgenemt('../test.txt')
#print(a.outputJSON())