import re, copy
from section_parser import parseSections


class Chapter:
    id = 0
    name = ""
    contents = []
    sections = []


def divideChapters(contents):
    begin_idx, end_idx = 0, 0
    chapter_pattern = re.compile("第\S+章\s+(\S+)")
    chapter_register = Chapter()

    chapters = []

    def isStartOfChapter(idx, contents):
        return chapter_pattern.match(contents[idx])

    def isEndOfChapter(idx, contents):
        return contents[idx] == "" and chapter_pattern.match(contents[idx + 1])

    def isEndOfContents(idx, contents):
        return idx == len(contents) - 1

    for idx, line in enumerate(contents):
        if isStartOfChapter(idx, contents):
            begin_idx = idx + 2
            chapter_register.id += 1
            chapter_register.name = chapter_pattern.match(line).group(1)
        elif isEndOfContents(idx, contents) or isEndOfChapter(idx, contents):
            end_idx = idx
            if isEndOfContents(idx, contents):
                end_idx += 1
            chapter_register.contents = contents[begin_idx: end_idx]
            chapters.append(copy.deepcopy(chapter_register))

    return chapters


def parseChapters(contents):
    chapters = divideChapters(contents)

    for chapter in chapters:
        chapter.sections = parseSections(chapter.contents)

    return chapters
