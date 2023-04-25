from functools import reduce
import re, docx

menu = list(map(lambda x: x.text.lstrip(), docx.Document("./目录.docx").paragraphs))


def filterOutNumber(line):
    return ''.join([i for i in line if not i.isdigit()])


def filterOutDots(line):
    tmp = re.sub("…+", "\t", line)
    # return re.sub("......", "\t", tmp)
    return tmp


def filterOutSpace(line):
    return ''.join([i for i in line if not i.isspace()])


menu = list(map(lambda line: filterOutNumber(line), menu))
menu = list(map(lambda line: filterOutDots(line), menu))
menu = list(filter(None, menu))
menu = reduce(lambda string, line: string + line, menu)
menu = menu.split("\t")
menu = list(map(lambda line: filterOutSpace(line), menu))
menu = list(filter(None, menu))