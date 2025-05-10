
import csv
from langdetect import detect
from collections import defaultdict
import json
# 创建一个默认字典来存储每种语言的计数
language_count = defaultdict(int)

# 打开CSV文件
with open('./data/UCAS_AISAD_TEXT-val.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        text = row[0]  # 假设文本在第一列
        try:
            language = detect(text)
            language_count[language] += 1
        except Exception as e:
            print(f'Error detecting language for text: {text} | Error: {str(e)}')

# 输出每种语言的数量
select_language = {}
for language, count in language_count.items():
    if count > 100:
        select_language[language] = count
        print(f'Language: {language} | Count: {count}')

with open('./data/languages-val.json', 'w', encoding='utf-8') as f:
    json.dump(select_language, f, ensure_ascii=False, indent=4)
