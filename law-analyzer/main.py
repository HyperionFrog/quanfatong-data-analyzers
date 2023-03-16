import copy
import json
import docx
import re
from cn2an import cn2an


# 所有实现遵循以可读性换性能的原则，不作过度优化
class Chapter:
    id = 0
    name = ""
    contents = []
    sections = []


class Section:
    id = 0
    name = ""
    contents = []
    articles = []

class Article:
    id = 0
    contents = []


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


def divideChapters(contents):
    begin_idx, end_idx = 0, 0
    chapter_pattern = re.compile("第\S+章\s+(\S+)")
    chapter_register = Chapter()

    chapters = []

    def isStartOfChapter(idx, contents):
        return chapter_pattern.match(contents[idx])

    def isEndOfChapter(idx, contents):
        return contents[idx] == "" and chapter_pattern.match(contents[idx + 1])

    for idx, line in enumerate(contents):
        if isStartOfChapter(idx, contents):
            begin_idx = idx + 2
            chapter_register.id += 1
            chapter_register.name = chapter_pattern.match(line).group(1)
        elif isEndOfChapter(idx, contents):
            end_idx = idx
            chapter_register.contents = contents[begin_idx: end_idx]
            chapters.append(copy.deepcopy(chapter_register))

    return chapters


def divideSections(contents):
    begin_idx, end_idx = 0, 0
    section_pattern = re.compile("第\S+节\s+(\S+)")
    section_register = Section()

    sections = []

    def isStartOfSection(idx, contents):
        return bool(section_pattern.match(contents[idx]))

    def isEndOfSection(idx, contents):
        try:
            return bool(contents[idx] == "" and section_pattern.match(contents[idx + 1]) or (idx + 1) == len(contents))
        except:
            pass

    for idx, line in enumerate(contents):
        if isStartOfSection(idx, contents):
            begin_idx = idx + 2
            section_register.id += 1
            section_register.name = section_pattern.match(line).group(1)
        elif isEndOfSection(idx, contents):
            end_idx = idx
            section_register.contents = contents[begin_idx: end_idx + 1]
            sections.append(copy.deepcopy(section_register))

    if len(sections) == 0:
        section_register.contents = contents
        sections.append(copy.deepcopy(section_register))

    return sections


def divideArticles(contents):
    begin_idx, end_idx = 0, 0
    article_pattern = re.compile("第(\S+)条\s+\S+")
    article_register = Article()

    articles = []

    def isStartOfArticle(idx, contents):
        return article_pattern.match(contents[idx])

    def isEndOfArticle(idx, contents):
        return idx == len(contents) - 1 or article_pattern.match(contents[idx + 1])

    for idx, line in enumerate(contents):
        if isStartOfArticle(idx, contents):
            begin_idx = idx
            article_register.id = cn2an(article_pattern.match(line).group(1))
        if isEndOfArticle(idx, contents):
            end_idx = idx
            article_register.contents = contents[begin_idx: end_idx + 1]
            article_register.contents[0] = re.match("第\S+条\s+(\S+)", article_register.contents[0]).group(1)
            articles.append(copy.deepcopy(article_register))

    return articles


def parseLaw(lines):
    title, contents = extractTitleAndContents(lines)
    chapters = divideChapters(contents)
    dic = {}
    output = []

    for chapter in chapters:
        parseChapter(chapter)

        for section in chapter.sections:
            for article in section.articles:
                dic["id"] = article.id
                dic["text"] = article.contents
                dic["chapter_id"] = chapter.id
                if section.name == "":
                    dic["hierarchy"] = [chapter.name]
                else:
                    dic["hierarchy"] = [chapter.name, section.name]
                dic["law"] = title
                output.append(copy.deepcopy(dic))

    return output


def parseChapter(chapter):
    chapter.sections = divideSections(chapter.contents)

    for section in chapter.sections:
        parseSection(section)


def parseSection(section):
    section.articles = divideArticles(section.contents)


if __name__ == '__main__':
    output_path = "./output.txt"
    doc = docx.Document("./assets/劳动合同法.docx")

    stripped_lines = list(map(lambda x: x.text.lstrip(), doc.paragraphs))
    output = parseLaw(stripped_lines)

    f = open(output_path, "w", encoding="utf-8")

    # 单行输出
    # f.write(json.dumps(output, ensure_ascii=False))

    # 多行输出
    for line in output:
        words = json.dumps(line, ensure_ascii=False)
        f.write(words)
        f.write('\n')

    f.close()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
