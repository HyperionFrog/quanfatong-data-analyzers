import operator

import pandas as pd
import json, os, concurrent.futures
from functools import reduce
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

    def isJudgement(clean_info):
        pattern = re.compile("判决书")

        return bool(pattern.search(clean_info["s1"]))

    def processInfo(raw_info):
        def map_fields(info_pair):
            if info_pair[0] in field_map:
                return (field_map.get(info_pair[0]), info_pair[1])

        def extractFieldsFromCourtInfo():
            dict_with_empty_pairs = map(map_fields, decoded_info.items())
            return dict(filter(None, dict_with_empty_pairs))

        def appendArticle():
            soup = BeautifulSoup(decoded_info["qwContent"], "lxml")
            text = filter(None, map(BeautifulSoup.getText, soup.find_all("div") + soup.find_all("p")))
            text = reduce(lambda s1, s2: s1 + '\n' + s2, text)
            dic["article"] = text

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
                except Exception:
                    raise RuntimeError("函数Run不了")

        decoded_info = json.loads(raw_info)
        if "qwContent" not in decoded_info:
            return None

        dic = extractFieldsFromCourtInfo()
        appendArticle()

        try:
            extractFieldsFromArticle()
        except RuntimeError:
            return None

        return dic

    list_of_judgements = list(filter(None, map(processInfo, tqdm(court_infos))))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(list_of_judgements, ensure_ascii=False, indent='\t'))


if __name__ == '__main__':
    assets_path = "assets/judgements"
    txt_files = [f for f in os.listdir(assets_path) if f.endswith('.txt')]
    count = 1
    for txt_file in txt_files:
        print(txt_file)
        txt_path = os.path.join(assets_path, txt_file)
        analyzeCourtInfo(txt_path, f"output{count}.json")
        count += 1
