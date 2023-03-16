import re, copy
from subpart_parser import parseSubparts


class Part:
    id = 0
    name = ""
    contents = []
    subparts = []


def divideParts(contents):
    begin_idx, end_idx = 0, 0
    part_pattern = re.compile("第[^分]+编\s+(\S+)")
    part_register = Part()

    parts = []

    def isStartOfPart(idx, contents):
        return part_pattern.match(contents[idx])

    def isEndOfPart(idx, contents):
        return contents[idx] == "" and part_pattern.match(contents[idx + 1])

    def isEndOfContents(idx, contents):
        return idx == len(contents) - 1

    for idx, line in enumerate(contents):
        if idx == 448:
            pass

        if isStartOfPart(idx, contents):
            begin_idx = idx + 2
            part_register.id += 1
            part_register.name = part_pattern.match(line).group(1)
        elif isEndOfContents(idx, contents) or isEndOfPart(idx, contents):
            end_idx = idx
            if (isEndOfContents(idx, contents)):
                end_idx += 1
            part_register.contents = contents[begin_idx: end_idx]
            parts.append(copy.deepcopy(part_register))

    return parts


def parseParts(contents):
    parts = divideParts(contents)

    for part in parts:
        part.subparts = parseSubparts(part.contents)

    return parts