import json
from openai import OpenAI
import random
import time
import os
# 从 JSON 文件读取字典
def set_seed(seed):
    random.seed(seed)

set_seed(42)
client = OpenAI(
    api_key="",
    base_url="",
)

def get_response(messages):
    try:
        print(messages)
        completion = client.chat.completions.create(
        model="gpt-4", # gpt-4-turbo gpt-3.5-turbo
        temperature=0,
        messages=messages,
        )
        time.sleep(1)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[Error] {e}")
        time.sleep(10)
        return get_response(messages)

def answer(input_file, output_file):
    templates = 'Please write a passage to answer the query in the corresponding language. \nLanguage: {language}\nQuery:{query}\nAnswer:'

    now_data = []
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = json.loads(line) 
                now_data.append(line['id'])
    with open(output_file, 'a+', encoding='utf-8') as w:
        with open(input_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = json.loads(line)  
                _id, query, lang = line['id'], line['query'], line['language']
                if _id in now_data:
                    continue
                print(query)
                llm_answer = get_response(messages = [{'role': 'user', 'content': templates.format(query=query, language=lang)}])
                print(llm_answer)
                line['llm_answer'] = llm_answer
                w.write(json.dumps(line, ensure_ascii=False) + '\n')

answer('./data/output.jsonl', './data/result.jsonl')