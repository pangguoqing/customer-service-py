import csv
import ast
from unittest import result
import numpy as np
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

class HistorysGetter:
    def __init__(self, api_key, embeddings_csv_file, embedding_engine="text-embedding-ada-002"):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.embeddings_csv_file = embeddings_csv_file
        self.processed_data = []
        self.embedding_engine = embedding_engine
        self.read_and_process_csv()  # 预缓存

    def read_and_process_csv(self, row_limit=1000):
        with open(self.embeddings_csv_file, 'r') as file:
            reader = csv.reader(file)
            for count, row in enumerate(reader):
                values_str = row[3]
                values_list = ast.literal_eval(values_str)  # 将字符串转换为实际的数值列表
                self.processed_data.append(row[:3] + [values_list])
                if count >= row_limit:
                    break

    def query(self, user_input, num=5):
        q_emb = get_embedding(user_input, engine=self.embedding_engine)
        sims = [cosine_similarity(q_emb, v[3]) for v in self.processed_data]
        sorted_indices = np.argsort(sims)[::-1]  # 获取排序后的索引，倒序排列
        top_indices = sorted_indices[:num]
        result = []
        for index in top_indices:
            result.append(self.processed_data[index][:3] + [sims[index]])
        return result

# # 使用示例：
# historys_getter = HistorysGetter('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', 'embeddings.csv')
# historys = historys_getter.query("用积分换的东西，比我平常在网上买的还贵")
