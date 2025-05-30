NaiLong Team

运行方法：
# 1. 安装llama-factory框架

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]" --no-build-isolation
```

# 2. 准备模型

 1. 下载到本地
```bash
git lfs install
git clone https://huggingface.co/Qwen/Qwen3-8B
```
 2. 直接使用模型仓库中的模型或者在线加载

# 3. 将数据放在llama-factory目录下

默认目录在detect下
```bash
cp ./data/final_sft_data.json ./LLaMA-Factory/data
cp ./config/put_data.py ./LLaMA-Factory/data
cd ./LLaMA-Factory/data
python put_data.py
```
需要修改.yaml配置文件中的model_path
```bash
cp ./config/qwen3_detect.yaml ./LLaMA-Factory/examples/train_full
```

# 4. 微调

默认使用4卡A100 80G
```bash
cd ./LLaMA-Factory
FORCE_TORCHRUN=1 llamafactory-cli train examples/train_full/qwen3_detect.yaml
```

# 5. 推理
```bash
cd ./predict
#更改predict中的model_path
python predict.py
```
