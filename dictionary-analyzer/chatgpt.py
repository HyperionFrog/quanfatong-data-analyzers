import os
import openai

# Configure proxy if you are running the script in mainland China
os.environ["HTTP_PROXY"] = "127.0.0.1:2081"
os.environ["HTTPS_PROXY"] = "127.0.0.1:2081"

openai.api_key = "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"


instructions = open("instructions.txt", "r", encoding="utf-8").read()


class ChatGPT:
    def __init__(self, conversation_list=[]) -> None:
        self.conversation_list = conversation_list
        self.conversation_list.append({"role": "user",
                                       "content": instructions})

    def respond(self, prompt):
        self.conversation_list.append({"role": "user",
                                       "content": prompt})

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)
        msg = response.choices[0].message['content']
        self.conversation_list.append({"role": "assistant", "content": msg})

        return msg

#
# bot = ChatGPT()
#
# while True:
#     message = input(f"\U0001f47b: ")
#     output_msg = f"\U0001f47D: {bot.respond(message)}"
#     print(output_msg)