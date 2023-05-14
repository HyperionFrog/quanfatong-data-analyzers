import json, os, re
import operator
import random
from functools import reduce

from tqdm import tqdm

from calc_sim import law_embe_dict

laws_path = 'assets/laws'
file_paths = [os.path.join(laws_path, filename) for filename in os.listdir(laws_path)]

search_engine = law_embe_dict(file_paths)

with open('output.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())

counter = 0


def processPojo(pojo):
    def processLawsPerChoice(choice_idx, laws):
        if not laws:
            return None

        ret_pojo = {}
        try:
            ret_pojo['input'] = f"有疑问：{pojo['timu']} {pojo['xuanxiang'][choice_idx]}\n\n有法条：\n"
        except IndexError:
            return None

        article_patterns = [f"{law} 第{idx}条" for (law, idx) in laws]
        sim_articles = search_engine.find(pojo['timu'], 50)

        articles_in_top50 = []
        has_at_least_one_match = False
        for article in sim_articles:
            is_match_found = False

            for pattern in article_patterns:
                match = re.match(pattern, article)
                if match:
                    is_match_found = True
                    break

            if is_match_found:
                has_at_least_one_match = True
                articles_in_top50.append(article)

        if not has_at_least_one_match:
            return None

        sim_articles = sim_articles[:7] + articles_in_top50
        random.shuffle(sim_articles)
        ret_pojo['input'] += reduce(operator.iadd, map(lambda article: article + '\n', sim_articles))
        ret_pojo['output'] = reduce(operator.iadd, [f"{law} 第{idx}条\n" for law, idx in laws])
        ret_pojo['output'].append('请你筛选出最有联系的法条')

        return ret_pojo

    global counter
    counter += 1

    if not pojo['laws']:
        return None

    ret_pojos = []
    for idx, law in enumerate(pojo['laws']):
        ret_pojos.append(processLawsPerChoice(idx, law))

    stream = list(filter(None, ret_pojos))

    return stream


output = []
for pojo in tqdm(data):
    if counter % 200 == 0:
        with open('training dataset.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(output, ensure_ascii=False, indent='\t'))

    ret_val = processPojo(pojo)
    if ret_val:
        output.extend(ret_val)


with open('training dataset.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(output, ensure_ascii=False, indent='\t'))
