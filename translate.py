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

lang_dict = {
    'en': 'English',
    'ru': 'Russian',
    'bg': 'Bulgarian',
    'zh-cn': 'Simplified Chinese',
    'id': 'Indonesian',
    'de': 'German'
}

def get_response(messages):
    try:
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

def translate_documents(input_file, output_file, language_ratios):
    templates = 'Please translate the text into {language}. \nText: {text} \nTranslated text:'

    now_data = []
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = json.loads(line) 
                now_data.append(line['id'])

    # 读取所有文档
    docs = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = json.loads(line)  
            docs[line['_id']] = {'query': line['text'], 'human_answer': line['human_answer']}

    translated_docs = []

    # 计算每种语言需要翻译的数量
    languages, weights = list(language_ratios.keys()), list(language_ratios.values())
    target_langs = random.choices(languages, weights=weights, k=len(docs))
    doc_with_target_lang = list(zip(list(docs.keys()), target_langs))

    # 随机选择文档进行翻译
    with open(output_file, 'a+', encoding='utf-8') as f:
        for doc_id, target_lang in doc_with_target_lang:
            if doc_id in now_data:
                continue
            if target_lang == 'en':
                result = {
                    'id': doc_id,
                    'query': docs[doc_id]['query'],
                    'human_answer': docs[doc_id]['human_answer'],
                    'language': target_lang
                }
            else:
                query, human_answer = docs[doc_id]['query'], docs[doc_id]['human_answer']
                translated_query = get_response(messages = [{'role': 'user', 'content': templates.format(language=lang_dict[target_lang], text=query)}])
                translated_answer = get_response(messages = [{'role': 'user', 'content': templates.format(language=lang_dict[target_lang], text=human_answer)}])
                result = {
                    'id': doc_id,
                    'query': translated_query,
                    'human_answer': translated_answer,
                    'language': target_lang
                }
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

with open('./data/languages-val.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
total_ratio = sum(data.values())

# 计算比例
language_proportions = {key: value / total_ratio for key, value in data.items()}

print(language_proportions)
# 使用示例
translate_documents('./data/nq_queries_w_doc.jsonl', './data/output.jsonl', language_proportions)