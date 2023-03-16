import re, copy
from article_parser import parseArticles


class Section:
    id = 0
    name = ""
    contents = []
    articles = []


def divideSections(contents):
    begin_idx, end_idx = 0, 0
    section_pattern = re.compile("第\S+节\s+(\S+)")
    section_register = Section()

    sections = []

    def isStartOfSection(idx, contents):
        return section_pattern.match(contents[idx])

    def isEndOfSection(idx, contents):
        return idx == len(contents) - 1 or contents[idx] == "" and section_pattern.match(contents[idx + 1])

    def isEndOfContents(idx, contents):
        return idx == len(contents) - 1

    for idx, line in enumerate(contents):
        if isStartOfSection(idx, contents):
            begin_idx = idx + 2
            section_register.id += 1
            section_register.name = section_pattern.match(line).group(1)
        elif isEndOfContents(idx, contents) or isEndOfSection(idx, contents):
            end_idx = idx
            if isEndOfContents(idx, contents):
                end_idx += 1
            section_register.contents = contents[begin_idx: end_idx]
            sections.append(copy.deepcopy(section_register))

    if len(sections) == 0:
        section_register.contents = contents
        sections.append(copy.deepcopy(section_register))

    return sections


def parseSections(contents):
    sections = divideSections(contents)

    for section in sections:
        section.articles = parseArticles(section.contents)

    return sections
