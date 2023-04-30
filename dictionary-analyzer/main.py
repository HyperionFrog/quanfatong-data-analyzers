import json, os
import re


dict_file = open("./dictionary.txt", "r", encoding="utf-8")
menu_file = open("./menu.txt", "r", encoding="utf-8")

lines = list(map(lambda line: line.rstrip(), dict_file.readlines()))
menu = list(map(lambda line: line.rstrip(), menu_file.readlines()))
output = []
version = 0

verbs = [
    "亦称", r"有.+义", r"与.+相对", "确定", r".+在.+上使用", r"与.+同义", "简称",
    "即", "指", "狭义指", "通常指", "在法律意义上指", "泛指", "特指", "广义指", "广义泛指",
    "在我国，指"
]


def hasVerb(line):
    global verbs
    for verb in verbs:
        if re.match(verb, line[:30]):
            return True

    return False


verb_output = []
non_verb_output = []
for line, term in zip(lines, menu):
    noun = term
    content = line[len(noun):]

    if term == "另行选举":
        pass

    if content.startswith("见") or content.startswith("详见"):
        continue

    if hasVerb(content):
        description = term + content
        verb_output.append({"content": f"请问什么是{noun}？", "summary": description})
    else:
        description = term + "是" + content
        non_verb_output.append({"content": f"请问什么是{noun}？", "summary": description})

output_file = open("verb_output.txt", "w", encoding="utf-8")
output_file.write(json.dumps(verb_output, ensure_ascii=False, indent="\t"))
output_file = open("non_verb_output.txt", "w", encoding="utf-8")
output_file.write(json.dumps(non_verb_output, ensure_ascii=False, indent="\t"))
