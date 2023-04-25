import os
import openai

# Configure proxy if you are running the script in mainland China
os.environ["HTTP_PROXY"] = "127.0.0.1:2081"
os.environ["HTTPS_PROXY"] = "127.0.0.1:2081"


class ChatGPT:
    keys = [
        "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",
        "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",
        "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",
        "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"
    ]
    key_idx = 0

    instructions = open("instructions.txt", "r", encoding="utf-8").read()

    def __init__(self, conversation_list=[]) -> None:
        self.conversation_list = conversation_list
        self.conversation_list.append({"role": "user",
                                       "content": self.instructions})
        openai.api_key = self.keys[2]

    def switchKey(self):
        self.key_idx += 1

        if self.key_idx >= len(self.keys):
            self.key_idx = 0

        openai.api_key = self.keys[self.key_idx]

    def respond(self, prompt):
        self.conversation_list.append({"role": "user",
                                       "content": prompt})

        while True:
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)
                msg = response.choices[0].message['content']
                self.conversation_list.append({"role": "assistant", "content": msg})

                if len(self.conversation_list) > 2:
                    self.conversation_list = [self.conversation_list[0]]

                return msg
            except openai.error.RateLimitError:
                print("Try another key\n")
                self.switchKey()
            except openai.error.APIConnectionError:
                print("Poor internet connection, retrying\n")
