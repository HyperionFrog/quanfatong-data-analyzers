import json
from chatgpt import ChatGPT

dict_file = open("./dictionary.txt", "r", encoding="utf-8")
output_file = open("./output.txt", "w", encoding="utf-8")

stripped_lines = list(dict_file.readlines())

bot = ChatGPT()

output = []

for line in stripped_lines:
    response = bot.respond(line)
    output.append(json.loads(response))
    print(response + "\n")