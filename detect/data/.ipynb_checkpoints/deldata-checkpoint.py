import json

with open('ai_text_detect.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in range(len(data)):
    last_char = data[i]["output"][-1]

# 更新 output 字段
    data[i]["output"] = last_char
    data[i]["problem"] = data[i]["instruction"] + "\n" + data[i]["input"]
    data[i]["answer"] = "<think> 无 </think>" + "<answer>" + data[i]["output"]+ "</answer>"

# 输出修改后的 JSON 数据
with open('text_detect.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)