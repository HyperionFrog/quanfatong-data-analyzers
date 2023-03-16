import re, copy
from chapter_parser import parseChapters


class Subpart:
    id = 0
    name = ""
    contents = []
    chapters = []


def divideSubparts(contents):
    begin_idx, end_idx = 0, 0
    subpart_pattern = re.compile("第\S+分编\s+(\S+)")
    subpart_register = Subpart()

    subparts = []

    def isStartOfSubpart(idx, contents):
        return subpart_pattern.match(contents[idx])

    def isEndOfSubpart(idx, contents):
        return contents[idx] == "" and subpart_pattern.match(contents[idx + 1])

    def isEndOfContents(idx, contents):
        return idx == len(contents) - 1

    for idx, line in enumerate(contents):
        if isStartOfSubpart(idx, contents):
            begin_idx = idx + 2
            subpart_register.id += 1
            subpart_register.name = subpart_pattern.match(line).group(1)
        elif isEndOfContents(idx, contents) or isEndOfSubpart(idx, contents):
            end_idx = idx
            if isEndOfContents(idx, contents):
                end_idx += 1
            subpart_register.contents = contents[begin_idx: end_idx]
            subparts.append(copy.deepcopy(subpart_register))

    return subparts


def parseSubparts(contents):
    subparts = divideSubparts(contents)

    for subpart in subparts:
        subpart.chapters = parseChapters(subpart.contents)

    return subparts
