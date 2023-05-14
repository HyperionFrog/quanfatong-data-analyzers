import json

from interact import embedding, interact
from tqdm import tqdm
import heapq
import time
import numpy as np


class law_embe_dict:
    def __init__(self, file_names):
        self.laws = []
        self.embeddings = []
        self.norm = []
        if hasattr(file_names, 'str'):
            file_names = [file_names]
        for file_name in tqdm(file_names):
            with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    json_obj = json.loads(line.strip())
                    try:
                        if json_obj['structure'][-1] == '条':
                            text = json_obj['name'] + ' 第' + str(json_obj['ids'][-1]) + '条 ' + json_obj['texts'][-1]
                            law_embedding = np.array(json_obj['embedding']) #question_embedding
                            self.laws.append(text)
                            self.embeddings.append(law_embedding)
                            self.norm.append(np.linalg.norm(law_embedding))
                    except:
                        None

    def find(self, text, top = 10):
        def cosine_similarity(a, b, norm_a, norm_b):
            dot_product = np.dot(a, b)
            return dot_product / (norm_a * norm_b)

        def update_text(text):
            prompt = f"我的问题与\"{text}\"有关\n请你输出，规范这一问题的法律的文本，可能是怎么样规定的，你只需要说出你猜测的法律规定的文本是长什么样的即可。"
            answer = interact(text)
            print(answer)
            return answer

        start_time = time.time()
        target_embedding = np.array(embedding(text))
        norm = np.linalg.norm(target_embedding)
        # print("embedding耗时=", time.time() - start_time)
        law_heap = []
        cos_sims = []

        start_time = time.time()
        for i in range(len(self.embeddings)):
            src_embedding = self.embeddings[i]
            cos_sim = cosine_similarity(target_embedding, src_embedding, norm, self.norm[i])
            cos_sims.append(cos_sim)
        end_time = time.time()
        # print("搜索耗时=", end_time - start_time)

        for i, cos_sim in enumerate(cos_sims):
            heapq.heappush(law_heap, (cos_sim, i))
            if len(law_heap) > top:
                heapq.heappop(law_heap)
        law_heap = sorted(law_heap, reverse=True)
        # print("排序耗时=", time.time() - end_time)

        sim_laws = [self.laws[i] for sim, i in law_heap]
        return sim_laws

    def find_exactly(self, text, top = 10):
        laws = self.find(text, top)
        for sim, law in laws:
            print(sim, law)
        problem = '有问题:' + text
        law_text = '下面是法条:\n' + '\n\n'.join([law for sim, law in laws])
        require = '''请你找出与该问题最有联系的法条并输出，你可以在一部或者多部法律中，找出一条或者多条法条。你输出法名和第多少条即可。'''
        prompt = '\n\n'.join([problem, law_text, require])
        useful_laws = interact(prompt)
        print(useful_laws)

        require = f'在句子"{useful_laws}"提取出法名和法条编号，并以json列表的输出，用name字段表示法条名字，用id表示第几条法(用纯阿拉伯数字表示)'
        answer = interact(require)
        print(answer)