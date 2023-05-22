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

query = "用积分换的东西，比我平常在网上买的还贵"
q_emb = get_embedding(query, engine="text-embedding-ada-002")

sims = [cosine_similarity(q_emb, v[3]) for v in processed_data]
sorted_indices = np.argsort(sims)[::-1]  # 获取排序后的索引，倒序排列

result = [processed_data[i] for i in sorted_indices]  # 根据索引顺序构建新的数组

first_column = [item[0] for item in result]  # 提取每个元素的第一列数据

first_5_rows = result[:5]  # 获取前10行数据

def append_similarity_values(rows, sims):
    new_rows = []
    for i, row in enumerate(rows):
        sim_value = sims[sorted_indices[i]]
        row_with_sim = row[:3] + [sim_value]
        new_rows.append(row_with_sim)
    return new_rows

# 调用示例
new_rows = append_similarity_values(first_5_rows, sims)
print(new_rows)

def query(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": """你现在是喜马拉雅的客服机器人，你掌握熟练的用户沟通技巧，能通过结合当前用户提供的求助/投诉信息和系统提供的过往相关的其它用户的求助/投诉案例，给出很专业建议。帮当前用户解决在平台上遇到的一系列问题。
             在回答的时候注意以下几个点：
             1.相似度信息：数值越接近1，相关度就越大。重点结合0.9以上的案例回答用户，0.9以下的可以做为辅助参考信息，0.8以下的信息参考意义不是很大
             2.时间信息：如果相似度差不多的案例，在给用户的反馈时表达的含义有冲突。重点结合时间相近的案例回答用户，时间相远的案例可以作为辅助参考信息
             3.商品：当前用户的信息可能包含商品字段，如果商品字段和案例里提到的商品不一致，请以当前用户信息里提供的商品为准，并不要再提到案例中的商品。
             4.请直接面向用户返回结果，回答的内容需要让用户感到舒服和被尊重，可以用“亲，”开头。
             5.回答的内容，不必提及其它案例相关的事情，因为这些信息用户看不到，也不能告知用户。
             """},
            {"role": "user", "content": text},
        ],
        temperature=0.1
    )
    summarized_text = response.get("choices")[0].get("message").get("content")
    return summarized_text

def convert_array_to_string(results):
    text = ""
    for i, result in enumerate(results):
        text += f"案例编号：{i + 1}\n用户的求助/诉求：{result[0]}\n给用户的反馈：{result[1]}\n时间：{result[2]}\n相似度：{result[3]}\n\n"
    return text

def prompt(user_input, historys):
    historys_str = convert_array_to_string(historys)
    text = f"""
当前用户：
用户的求助/诉求：{user_input}
商品：篮球
时间：20230514 22:00

{historys_str}
"""
    print(text)
    return text

output_text = query(prompt( "用积分换的东西，比我平常在网上买的还贵", new_rows))

print("返回: ", output_text)

