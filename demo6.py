import csv
import re
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import numpy as np
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

processed_data = []  # 用于存储处理后的数据

with open('demo6.csv', 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        row0 = row[0] 
        emb = get_embedding(row0)
    
        processed_row = [row[0]] + [row[1]] + [row[2]] + [emb]
        processed_data.append(processed_row)

with open('demo6_output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(processed_data)  # 写入处理后的数据
    
    
query = "耳机X2，是送我两个吗"
q_emb = get_embedding(query)

sims = [cosine_similarity(q_emb, v[3]) for v in processed_data]

print(sims)