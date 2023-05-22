import openai
from historys_getter import HistorysGetter
import time

class ChatAssistant:
    def __init__(self, api_key, embeddings_csv_file):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.history_getter = HistorysGetter(api_key, embeddings_csv_file)

    def query(self, user_input, order_info):
        t = time.time()
        historys = self.history_getter.query(user_input)
        # print('chat_1', time.time() - t)
        historys_text = self.convert_historys_to_text(historys)
        # print('chat_2', time.time() - t)
        order_info_text = self.convert_order_info_to_text(order_info)
        # print('chat_3', time.time() - t)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """你现在是喜马拉雅的客服机器人，你掌握熟练的用户沟通技巧，能通过结合订单信息、过往相关的其它用户的求助/投诉案例，给出很专业建议。帮当前用户解决在平台上遇到的一系列问题。
                在回答时请注意以下几点：
                1.案例的相似度信息：数值越接近1，表示相关度越大。重点参考相似度高于0.9的案例来回答用户问题，0.9以下的案例可以作为辅助参考信息，0.8以下的案例参考意义较小。
                2.案例的时间信息：如果相似度相近的案例给出的反馈有冲突，重点参考时间相近的案例来回答用户，时间较远的案例可以作为辅助参考信息。
                3.商品信息：商品的信息以订单信息中提到的为准，因为用户有时候会写错商品信息。
                4.请直接回答用户问题，并以亲切和尊重的方式进行表达，可以用“亲，”开头。
                5.回答的内容，不能提及其它案例相关的事情，因为这些信息当前用户看不到，也不能告知用户。
                6.如果没有找到高度相关的案例，必要时可以提醒用户联系客服
                """},
                {"role": "user", "content": "请从查询一下跟当前咨询相关的订单信息"},
                {"role": "assistant", "content": order_info_text},
                {"role": "user", "content": "请从查询一下跟当前咨询存在一定相关度的其它用户的过往案例"},
                {"role": "assistant", "content": historys_text},
                {"role": "user", "content": user_input},
            ],
            temperature=0.1,
            max_tokens=100,
        )
        # print('chat_4', time.time() - t)
        summarized_text = response.choices[0].message.content
        print(response.usage)
        return summarized_text
    
    def convert_order_info_to_text(self, order_info):
        return f"订单编号：{order_info.get('id')},商品名称：{order_info.get('product')},时间：{order_info.get('at')}"

    def convert_historys_to_text(self, historys):
        text = ""
        for i, history in enumerate(historys):
            text += f"案例编号：{i + 1}\n用户的求助/诉求：{history[0]}\n平台给用户的反馈：{history[1]}\n时间：{history[2]}\n相似度：{history[3]}\n\n"
        print('相关案例', text)
        return text

# # 使用示例：
# chat_assistant = ChatAssistant('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', 'embeddings.csv')
# output_text = chat_assistant.query("用积分换的东西，比我平常在网上买的还贵")
