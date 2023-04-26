import json, os
import re

from chatgpt import ChatGPT

dict_file = open("./dictionary.txt", "r", encoding="utf-8")
menu_file = open("./menu.txt", "r", encoding="utf-8")

lines = list(map(lambda line: line.rstrip(), dict_file.readlines()))
menu = list(map(lambda line: line.rstrip(), menu_file.readlines()))
bot = ChatGPT()
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
        verb_output.append({"noun": noun, "description": description})
    else:
        description = term + "是" + content
        non_verb_output.append({"noun": noun, "description": description})

output_file = open("verb_output.txt", "w", encoding="utf-8")
output_file.write(json.dumps(verb_output, ensure_ascii=False, indent="\t"))
output_file = open("non_verb_output.txt", "w", encoding="utf-8")
output_file.write(json.dumps(non_verb_output, ensure_ascii=False, indent="\t"))

# def loadLatestVersion():
#     global version
#     files = [f for f in os.listdir("./assets/") if f.endswith('.txt')]
#     for file in files:
#         version = max(version, int(re.match(r"output_(\d+).txt", file).group(1)))
#
#
# def save():
#     global version
#     output_file = open("./output.txt", "w", encoding="utf-8")
#     output_file.write(json.dumps(output, ensure_ascii=False, indent="\t"))
#     output_file.close()
#
#     output_file = open(f"./assets/output_{version + 1}.txt", "w", encoding="utf-8")
#     output_file.write(json.dumps(output, ensure_ascii=False, indent="\t"))
#     output_file.close()
#     version += 1
#
#
# def reload():
#     global output, lines
#     if version > 0:
#         previous_answers = json.loads(open(f"./assets/output_{version}.txt", "r", encoding="utf-8").read())
#         output = previous_answers
#         lines = lines[len(output):]
#
#
# def askGPT():
#     count = 0
#     for line in lines:
#         response = bot.respond(line)
#         print(response + "\n")
#         output.append(json.loads(response))
#         count += 1
#
#         if count >= 9:
#             save()
#             reload()
#             return
#
#
# loadLatestVersion()
# reload()
#
# while True:
#     askGPT()
