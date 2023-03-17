import json, docx, re, copy
from part_parser import parseParts


# 所有实现遵循以可读性换性能的原则，不作过度优化


def extractTitleAndContents(lines):
    begin_idx, end_idx, title_idx = -1, -1, -1
    title_pattern = re.compile(r"法|条例|解释|办法")
    title = ""

    for idx, line in enumerate(lines):
        if (begin_idx == -1):
            if (title_pattern.findall(line)):
                if len(title) == 0:
                    title = line
                    title_idx = idx
            elif (line == "目　　录"):
                begin_idx = idx + 1
            else:
                continue
        else:
            if (line == ""):
                end_idx = idx
                break
            else:
                continue
    if end_idx == -1:
        end_idx = title_idx

    return title, lines[end_idx + 1:]


def parseLaw(lines):
    title, contents = extractTitleAndContents(lines)
    parts = parseParts(contents)
    dic = {}
    output = []

    for part in parts:
        for subpart in part.subparts:
            for chapter in subpart.chapters:
                for section in chapter.sections:
                    for article in section.articles:
                        dic["id"] = article.id
                        dic["text"] = list(filter(lambda x: x != "", article.contents))
                        dic["chapter_id"] = list(filter(None, [part.id, subpart.id, chapter.id, section.id]))
                        dic["hierarchy"] = list(filter(None, [part.name, subpart.name, chapter.name, section.name]))
                        dic["law"] = title
                        output.append(copy.deepcopy(dic))

    return output


if __name__ == '__main__':
    output_path = "./output.txt"
    doc = docx.Document("./assets/民法典.docx")

    stripped_lines = list(map(lambda x: x.text.lstrip(), doc.paragraphs))
    output = parseLaw(stripped_lines)

    f = open(output_path, "w", encoding="utf-8")

    f.write(json.dumps(output, ensure_ascii=False, indent="\t"))

    f.close()
