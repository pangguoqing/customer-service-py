import csv
import re
import time
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import numpy as np
import os

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

processed_data = []  # 用于存储处理后的数据
output_file = 'demo7_output.csv'  # 输出文件名
batch_size = 1  # 每批处理的数据量
rest_time = 2  # 休息时间（秒）
# resume_from_line = 321  # 指定从哪一行开始继续处理数据

if not os.path.exists(output_file):
    open(output_file, 'w').close()

# 读取已处理的数据行数
processed_lines = 1233
# with open(output_file, 'r') as processed_file:
#     processed_reader = csv.reader(processed_file)
#     processed_lines = sum(1 for _ in processed_reader)

# 读取输入文件，并从指定行开始处理数据
with open('demo7.csv', 'r') as file:
    reader = csv.reader(file)
    
    # 跳过已处理的行数
    for _ in range(processed_lines):
        next(reader)
    
    # 处理剩余的数据
    for i, row in enumerate(reader, start=processed_lines):
        row0 = row[0] 
        print(row0)
        emb = get_embedding(row0, engine="text-embedding-ada-002")
        # emb = f"emb{i}"
    
        processed_row = [row[0]] + [row[1]] + [row[2]] + [emb]
        processed_data.append(processed_row)
        
        # 每处理完一批数据，保存到输出文件并休息5秒
        if (i + 1) % batch_size == 0:
            with open(output_file, 'a', newline='') as output:
                writer = csv.writer(output)
                writer.writerows(processed_data)
            processed_data = []  # 清空已处理数据列表
            
            print(f"已处理 {i+1} 行数据")
            
            if (i + 1) % (batch_size) == 0:
                print(f"休息 {rest_time} 秒")
                time.sleep(rest_time)
    
    # 处理剩余的数据，保存到输出文件
    if processed_data:
        with open(output_file, 'a', newline='') as output:
            writer = csv.writer(output)
            writer.writerows(processed_data)
        print(f"已处理 {i+1} 行数据")
