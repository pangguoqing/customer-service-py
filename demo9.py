# A: Let's think step by step
# 用精炼的文本来概括整篇文章的大意，使得用户能够通过阅读摘要来大致了解文章的主要内容
import csv
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import ast
import numpy as np

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

def query(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": """你现在是喜马拉雅的客服机器人，你掌握熟练的用户沟通技巧，能通过结合当前用户求助/投诉信息和过往相关的其它用户的求助/投诉案例，给出很专业建议。帮当前用户解决在平台上遇到的一系列问题。
             在回答的时候注意以下几个点：
             1.相似度信息：数值越接近1，相关度就越大。重点结合0.9以上的案例回答用户，0.9以下的可以做为辅助参考信息，0.8以下的信息参考意义不是很大
             2.时间信息：如果相似度差不多的案例，在给用户的反馈时表达的含义有冲突。重点结合时间相近的案例回答用户，时间相远的案例可以作为辅助参考信息
             3.请直接面向用户返回结果，回答的内容需要让用户感到舒服和被尊重，可以用“亲，”开头。
             4.回答的内容，不必提及其它案例相关的事情，因为用户不必知道。
             """},
            {"role": "user", "content": text},
        ],
        temperature=0.1
    )
    summarized_text = response.get("choices")[0].get("message").get("content")
    return summarized_text

text = """
当前用户：
用户的求助/诉求：耳机X2，是送我两个吗
时间：20230514 22:00

案例一：
用户的求助/诉求：×2是送两套耳机吗
给用户的反馈：这个是耳机型号哦
时间：20230411 17:02:04
相似度：0.9494958143084193

案例二：
用户的求助/诉求：耳机X2是什么意思
给用户的反馈：X2是型号哦
时间：20230409 22:38:18
相似度：0.9221803223999827

案例三：
用户的求助/诉求：漫步者耳机×2是两只耳机还是两个
给用户的反馈：两只耳机
时间：20230228 09:44:10
相似度：0.9129403569127765

案例四：
用户的求助/诉求：耳机可以买一个吗
给用户的反馈：耳机暂不支持单买哦
时间：20230326 17:56:28
相似度：0.898320248753776

案例五：
用户的求助/诉求：续费的238耳机x2是两对吗电商
给用户的反馈：这个是耳机型号的哦
时间：20230402 08:30:09
相似度：0.8942014314606468
"""
output_text = query(text)

print("请求: ", "耳机X2，是送我两个吗")
print("返回: ", output_text)