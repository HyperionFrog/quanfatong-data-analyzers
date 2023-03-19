import json, os


def processRawText(txt_path):
    with open(txt_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

        # 将数据分成两列
        id = []
        is_active = []

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
            id.append(lines[i].strip())
            is_active.append(lines[i + 1].strip())

        # 将结果写入输出文件
        output = list(map(lambda x, y: {"id": x, "is_active": y}, id, is_active))
        with open('E:/output.txt', 'w', encoding="utf-8") as f:
            f.write(json.dumps(output, ensure_ascii=False, indent="\t"))

        return output


def writeJsonToFiles():
    assets_path = "./assets"

    raw_text_files = [f for f in os.listdir(assets_path) if f.endswith('.txt')]

    for raw_text_file in raw_text_files:
        form_path = f"{assets_path}/{raw_text_file}"
        output = processRawText(form_path)
        output_path = f"./output/{raw_text_file}"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(output, ensure_ascii=False, indent='\t'))
