import json, os
import re

from chatgpt import ChatGPT

dict_file = open("./dictionary.txt", "r", encoding="utf-8")

lines = list(dict_file.readlines())
bot = ChatGPT()
output = []
version = 0


def loadLatestVersion():
    global version
    files = [f for f in os.listdir("./assets/") if f.endswith('.txt')]
    for file in files:
        version = max(version, int(re.match(r"output_(\d+).txt", file).group(1)))


def save():
    global version
    output_file = open("./output.txt", "w", encoding="utf-8")
    output_file.write(json.dumps(output, ensure_ascii=False, indent="\t"))
    output_file.close()

    output_file = open(f"./assets/output_{version + 1}.txt", "w", encoding="utf-8")
    output_file.write(json.dumps(output, ensure_ascii=False, indent="\t"))
    output_file.close()
    version += 1


def reload():
    global output, lines
    previous_answers = json.loads(open(f"./assets/output_{version}.txt", "r", encoding="utf-8").read())
    output = previous_answers
    lines = lines[len(output):]


def askGPT():
    count = 0
    for line in lines:
        response = bot.respond(line)
        print(response + "\n")
        output.append(json.loads(response))
        count += 1

        if count >= 9:
            save()
            reload()
            return


loadLatestVersion()
reload()

while True:
    askGPT()
