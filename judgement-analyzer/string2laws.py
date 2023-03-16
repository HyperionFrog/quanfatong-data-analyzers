# Author: AlphaINF

class string2laws:
    law_name = ""
    law_list = []

    def full_width_punctuation(self, text):
        # 定义半角字符和对应的全角字符
        punc_map = {
            ',': '，',
            '.': '。',
            ';': '；',
            ':': '：',
            '?': '？',
            '!': '！',
            '(': '（',
            ')': '）',
            '[': '【',
            ']': '】',
            '{': '｛',
            '}': '｝',
            '<': '〈',
            '＜': '〈',
            '>': '〉',
            '＞':'〉'
        }

        # 创建字符映射表
        punc_map_table = str.maketrans(''.join(punc_map.keys()), ''.join(punc_map.values()))

        # 应用字符映射表
        return text.translate(punc_map_table)

    def num_to_chinese_str(self, num):
        """
        将数字转换为汉字字符串
        :param num: int, 要转换的数字，范围在 0-9999 之间
        :return: str, 汉字字符串
        """
        if num < 0 or num > 9999:
            raise ValueError("数字超出范围，应为 0-9999 之间")

        chinese_chars = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        chinese_units = ['', '十', '百', '千', '万']

        res = ''
        if num == 0:
            return '零'

        if num >= 1000:
            res += chinese_chars[num // 1000] + chinese_units[3]
            num %= 1000
        if num >= 100:
            res += chinese_chars[num // 100] + chinese_units[2]
            num %= 100
        if num >= 10:
            if num // 10 != 1:
                res += chinese_chars[num // 10] + chinese_units[1]
            else:
                res += chinese_units[1]
            num %= 10
        if num > 0:
            res += chinese_chars[num]

            # 去掉“一十”中的“一”
        if res.startswith('一十'):
            res = res[1:]
        return res

    def cn_to_num(self, cn):
        if cn.startswith('十'):
            cn = '一' + cn
        num_dict = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                    '十': 10, '百': 100, '千': 1000, '万': 10000}
        cn_len = len(cn)
        num = 0
        tmp = 0
        b_unit = False  # 标识上一个字符是否为单位
        for i in range(cn_len):
            char = cn[i]
            if char in num_dict:
                val = num_dict[char]
                if val == 10 or val == 100 or val == 1000:
                    if i == 0 or b_unit:  # 首位为单位或上一个为单位，则不累加
                        b_unit = True
                    else:
                        b_unit = True
                        tmp = tmp * val
                        num += tmp
                        tmp = 0
                elif val == 10000:
                    b_unit = True
                    tmp = tmp * val
                    num += tmp
                    tmp = 0
                else:
                    b_unit = False
                    tmp = tmp + val
            else:  # 非数字
                return None
        num += tmp
        return num

    def __init__(self,string):
        self.law_name = ""
        self.law_list = []

        string = self.full_width_punctuation(string)

        name_first = string.find('《')
        name_last = string.find('》')

        self.law_name = string[name_first + 1: name_last]
        details = string[name_last+1:].split('、')

        tags = ['条','款','项']
        last_answer = [0, 0, 0]

        for detail in details:
            detail = detail.replace('（','')
            detail = detail.replace('）', '')
            answer = []
            for tag in tags:
                id = detail.find(tag)
                if id != -1:
                    sta = detail.find('第')
                    answer.append(self.cn_to_num(detail[sta+1:id]))
                    detail = detail[id+1:]
                else:
                    answer.append(0)

            if answer[0] == 0:
                answer[0] = last_answer[0]
                if answer[1] == 0:
                    answer[1] = last_answer[1]

            last_answer = answer
            if answer[2] == 0:
                answer.pop(2)
            if answer[1] == 0:
                answer.pop(1)
            self.law_list.append(answer)

    def outall(self):
        answers = []
        for one in self.law_list:
            answer = '《' + self.law_name + '》' + str(one)
            answers.append(answer)
        return answers

    def outall_simple(self):
        answers = []
        for one in self.law_list:
            one = one[0]
            try:
                answer = '《' + self.law_name + '》第' + self.num_to_chinese_str(one) + "条"
                answers.append(answer)
            except:
                answer = ''
        return answers

