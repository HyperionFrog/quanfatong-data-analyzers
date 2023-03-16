import json

#抽取jsonl中的所有公司名
def extract_and_filter_companies(jsonl_file):
    filtered_companies = []
    with open(jsonl_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            data = json.loads(line)
            plaintiff = data.get('plaintiff', [])
            defendant = data.get('defendant', [])

            filtered_plaintiff = [item for item in plaintiff if '公司' in item]
            filtered_defendant = [item for item in defendant if '公司' in item]

            filtered_companies += filtered_plaintiff + filtered_defendant

    filtered_companies = list(set(filtered_companies))

    with open('company.txt', 'w', encoding='utf-8', errors='ignore') as file:
        txt = '\n'.join(filtered_companies)
        file.write(txt)

extract_and_filter_companies('jsonl_file-last.jsonl')