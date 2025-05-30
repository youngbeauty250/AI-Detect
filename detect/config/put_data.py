import json

def add_new_dataset(json_path, new_dataset_name, file_name):
    """
    在 JSON 文件的根节点添加一个新的数据集条目。

    参数:
        json_path (str): JSON 文件路径。
        new_dataset_name (str): 新增的数据集名称 (如 "my_new_dataset")。
        file_name (str): 数据集对应的文件名 (如 "my_new_dataset.json")。
        file_sha1 (str): 数据集对应文件的 SHA-1 哈希值。
    """
    # 1. 读取 JSON 文件
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # 2. 新增数据集节点
    data[new_dataset_name] = {
        "file_name": file_name
    }
    
    # 3. 写回 JSON 文件
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    file_name = "final_sft_data"
    file_path = file_name + ".json"  # 替换为你的文件路径   

    # 假设已有 JSON 文件名为 "datasets.json"
    json_file_path = "dataset_info.json"
    
    # 新增的数据集信息
    dataset_key = file_name
    new_file_name = file_path
    
    # 调用函数新增数据集节点
    add_new_dataset(json_file_path, dataset_key, new_file_name)
    print(f"已在 {json_file_path} 中添加新数据集 {dataset_key}.")
