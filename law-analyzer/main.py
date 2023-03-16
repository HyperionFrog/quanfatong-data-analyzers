import json, docx, re, copy
from part_parser import parseParts


# 所有实现遵循以可读性换性能的原则，不作过度优化


def extractTitleAndContents(lines):
    begin_idx, end_idx = -1, -1
    title_pattern = re.compile("中华人民共和国(\S+法)")
    title = ""

    for idx, line in enumerate(lines):
        if (begin_idx == -1):
            if (title_pattern.match(line)):
                title = title_pattern.match(line).group(1)
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
                        dic["text"] = article.contents
                        dic["chapter_id"] = chapter.id
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
