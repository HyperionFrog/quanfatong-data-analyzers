import json

# 读取jsonl文件
input_file_path = '一审.txt'
output_file_path = '一审(劳动争议).txt'

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        # 将每一行解析成json对象
        json_obj = json.loads(line)

        # 判断case_type字段是否为"劳动争议"
        if json_obj.get('case_type') == '劳动争议':
            # 将满足条件的json对象写入到输出文件
            output_file.write(json.dumps(json_obj, ensure_ascii=False))
            output_file.write('\n')
