import csv
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import ast
import numpy as np

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

processed_data = []  # 用于存储处理后的数据

with open('demo8.csv', 'r') as file:
    reader = csv.reader(file)
    count = 0  # 计数器，记录已读取的行数

    for row in reader:
        values_str = row[3]  # 获取第4列的字符串
        values_list = ast.literal_eval(values_str)  # 将字符串转换为实际的数值列表

        processed_data.append(row[:3] + [values_list])
        count += 1

        if count >= 1000:  # 读取了10行后终止循环
            break

query = "耳机X2，是送我两个吗"
q_emb = get_embedding(query, engine="text-embedding-ada-002")

sims = [cosine_similarity(q_emb, v[3]) for v in processed_data]
sorted_indices = np.argsort(sims)[::-1]  # 获取排序后的索引，倒序排列

result = [processed_data[i] for i in sorted_indices]  # 根据索引顺序构建新的数组

first_column = [item[0] for item in result]  # 提取每个元素的第一列数据

first_10_rows = result[:10]  # 获取前10行数据

for i, row in enumerate(first_10_rows):
    sim_value = sims[sorted_indices[i]]  # 获取对应行的相似度值
    print(row[:3] + [sim_value])  # 打印前3列数据和相似度值


