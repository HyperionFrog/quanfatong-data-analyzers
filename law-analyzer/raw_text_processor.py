import json, os


def processRawText(input_path):
    with open(input_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

        # 将数据分成两列
        column1 = []
        column2 = []

        # idx val
        # 0   劳动法
        # 1
        # 2   编号
        # 3   是否使用
        # 4   1
        # 5   0
        # 6   2
        # 7   0

        for i in range(4, len(lines), 2):
            column1.append(lines[i].strip())
            column2.append(lines[i + 1].strip())

        # 将结果写入输出文件
        output = list(map(lambda x, y: {"id": x, "is_active": y}, column1, column2))
        with open('E:/output.txt', 'w', encoding="utf-8") as f:
            f.write(json.dumps(output, ensure_ascii=False, indent="\t"))

        return output


assets_path = "./assets"

form_files = [f for f in os.listdir(assets_path) if f.endswith('.txt')]

for form_file in form_files:
    form_path = f"{assets_path}/{form_file}"
    output = processRawText(form_path)
    output_path = f"./output/{form_file}"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(output, ensure_ascii=False, indent='\t'))
