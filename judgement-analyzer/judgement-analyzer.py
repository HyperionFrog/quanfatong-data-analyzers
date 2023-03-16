import pandas as pd
import json
from bs4 import BeautifulSoup

from judgements_prework import *
from entity_load import *
from functools import *


def analyzeCourtInfo(input_path, output_path):
    court_info = pd.read_csv(input_path, sep="\t")["CourtInfo"]

    field_map = {
        "s1": "name",
        "s2": "court",
        "s8": "type",
        "s9": "level",
        "s31": "time",
    }

    # judgement_funcs = {judge.get_plaintiff, judge.get_defendant, judge.get_claim
    #     , judge.get_answer, judge.get_case_type, judge.get_think
    #     , judge.get_complaint, judge.get_laws}

    def isJudgement(clean_info):
        pattern = re.compile("判 决 书")
        try:
            if pattern.search(clean_info["article"]):
                return True
            else:
                return False
        except:
            print(clean_info)

    def processInfo(raw_info):
        def map_fields(info_pair):
            if info_pair[0] in field_map:
                return (field_map.get(info_pair[0]), info_pair[1])

        def extractFieldsFromCourtInfo():
            dict_with_empty_pairs = map(map_fields, decoded_info.items())
            return dict(filter(None, dict_with_empty_pairs))

        def appendArticle():
            soup = BeautifulSoup(decoded_info["qwContent"], "lxml")
            text_with_empty_elements = map(lambda x: x.string, soup.find_all("div") + soup.find_all("p"))
            text = list(filter(None, text_with_empty_elements))

            dic["article"] = reduce(lambda str1, str2: str1 + "\n" + str2, text)

        def extractFieldsFromArticle():
            judge = Judgenemt(dic["article"].split("\n"))
            methods_for_fields = {
                "plaintiff": judge.get_plaintiff,
                "defendant": judge.get_defendant,
                "claim": judge.get_claim,
                "answer": judge.get_answer,
                "case_type": judge.get_case_type,
                "think": judge.get_think,
                "complaint": judge.get_complaint,
                "laws": judge.get_laws
            }

            for key, func in methods_for_fields.items():
                try:
                    dic[key] = func()
                except:
                    raise ValueError("函数Run不了")

        decoded_info = json.loads(raw_info)
        if "qwContent" not in decoded_info:
            return None

        dic = extractFieldsFromCourtInfo()
        appendArticle()

        if not isJudgement(dic):
            return None

        try:
            extractFieldsFromArticle()
        except ValueError:
            return None

        return dic

    list_of_judgements = filter(None, map(processInfo, court_info))

    #for val in list_of_judgements:

    #print(list_of_judgements)

    #df = pd.DataFrame(list_of_judgements)
    #print(df)
    #results = df.head(10).to_json(orient="records", force_ascii=False)

    f = open(output_path, "w", encoding="utf-8")

    for line in list_of_judgements:
        words = json.dumps(line, ensure_ascii=False)
        f.write(words)
        f.write('\n')

    f.close()


analyzeCourtInfo("E:\wenshu_new2022docId11.txt", "result.txt")
