import random, os

__sk_list = ['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']

os.environ["HTTP_PROXY"] = "127.0.0.1:2081"
os.environ["HTTPS_PROXY"] = "127.0.0.1:2081"

def interact(prompt, penalty = {}):
    import openai
    openai.api_key = random.choice(__sk_list)
    if isinstance(prompt, list):
        messages = prompt
    else:
        messages = [{"role": "user", "content": prompt}]

    out = ''
    for message in messages:
        if message['role'] == 'assistant':
            out = out + '有知识：' + message['content'] + '\n'
        else:
            out = out + message['content'] + '\n'
    #print(out)

    while True:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=messages,
                logit_bias = penalty,
                temperature=0
            )
            break
        except:
            from time import sleep
            sleep(0.2)

    answer = completion.choices[0].message['content']
    return answer

def embedding(text):
    import openai
    openai.api_key = random.choice(__sk_list)
    completion = openai.Embedding.create(
      model="text-embedding-ada-002",
      input=text
    )
    return completion['data'][0]['embedding']
