import re
from functools import reduce
import docx

doc = docx.Document("辞典.docx")

stripped_lines = list(filter(None, map(lambda line: line.text.rstrip(), doc.paragraphs)))

menu_file = open("menu.txt", "r", encoding="utf-8")
menu = list(map(lambda line: line.rstrip(), menu_file.readlines()))

title_file = open("titles.txt", "r", encoding="utf-8")
titles = list(map(lambda line: line.rstrip(), title_file.readlines()))

menu_idx = 0

max_title_len = 0
for title in titles:
    max_title_len = max(max_title_len, len(title))


def findLastNonBlankLine(lines, idx):
    while True:
        if lines[idx] == "":
            idx -= 1
        else:
            return idx


line_idx = 0
while line_idx < len(stripped_lines):
    line = stripped_lines[line_idx]

    def spiltMisConcatenatedLines():
        last_line = stripped_lines[line_idx - 1]
        start_idx_of_missing_line = last_line.find(menu[menu_idx])
        missing_line = last_line[start_idx_of_missing_line:]
        stripped_lines[line_idx - 1] = last_line[:start_idx_of_missing_line]
        stripped_lines.insert(line_idx, missing_line)

    def concatBrokenLines():
        stripped_lines[line_idx - 1] += line
        stripped_lines.pop(line_idx)

    if len(line) <= max_title_len and line in titles:
        stripped_lines.pop(line_idx)
    elif line.startswith(menu[menu_idx]):
        line_idx += 1
        menu_idx += 1
    elif line.startswith(menu[menu_idx + 1]):
        spiltMisConcatenatedLines()
    else:
        concatBrokenLines()

dict_file = open("dictionary.txt", "w", encoding="utf-8")
for line in filter(None, stripped_lines):
    dict_file.write(line + "\n")
dict_file.close()