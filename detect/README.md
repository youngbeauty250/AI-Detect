NaiLong Team
数据处理：采用俊哥的方案，使用final_data_process.py把output格式改成只有0和1，结果在data/final_sft_data.json
sft：采用llama-factory框架，使用Qwen3-8B，4卡A100
推理：prediction/prediction.py 微调后观察输出，有“1”和“ 0”两种输出形式，因此设置max_new_tokens设置为2，对于每个位置只考虑0和1的概率（0的token_id是15，1是16），然后softmax，输出时输出模型输出1或0位置的prob（对于“ 0”选择第二个位置，“1”选择第一个位置）