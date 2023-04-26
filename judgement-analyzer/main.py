import pandas as pd
import json
import os
from bs4 import BeautifulSoup

from entity_load import *
from tqdm import tqdm


def analyzeCourtInfo(input_path, output_path):
    court_infos = pd.read_csv(input_path, sep="\t")["CourtInfo"]

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
        pattern = re.compile("判决书")
        try:
            if pattern.search(clean_info["s1"]):
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
            line_elements = soup.find_all("div")
            texts = []
            for line in line_elements:
                text = line.text
                text = text.split('\n')
                texts.extend(text)
                #texts.append(text)

            dic["article"] = texts


            #soup = BeautifulSoup(decoded_info["qwContent"], 'html.parser').get_text()
            #dic["article"] = soup

        def extractFieldsFromArticle():
            judge = Judgenemt(dic["article"])
            methods_for_fields = {
                "plaintiff": judge.get_plaintiff,
                "defendant": judge.get_defendant,
                "case_type": judge.get_case_type,
                "claim": judge.get_claim,
                "complaint": judge.get_complaint,
                "answer": judge.get_answer,
                "think": judge.get_think,
                "laws": judge.get_laws,
                "judge": judge.get_judge,
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

        #if not isJudgement(dic):
        #    return None

        try:
            extractFieldsFromArticle()
        except ValueError:
            return None

        return dic

    list_of_judgements = []
    for court_info in tqdm(court_infos):
        out = processInfo(court_info)
        list_of_judgements.append(out)

    list_of_judgements = list(filter(None,list_of_judgements))

    with open(output_path, "a", encoding="utf-8") as f:
        for judgement in list_of_judgements:
            json_line = json.dumps(judgement, ensure_ascii=False)
            f.write(json_line + "\n")

if __name__ == '__main__':
    assets_path = "./judge_input"
    txt_files = [f for f in os.listdir(assets_path) if f.endswith('.txt')]
    for txt_file in txt_files:
        print(txt_file)
        txt_path = os.path.join(assets_path, txt_file)
        analyzeCourtInfo(txt_path, "output.txt")
