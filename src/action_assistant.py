import openai
from historys_getter import HistorysGetter

class ActionAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def query(self, user_input, chat_assistant_output):
        actions = [{"id": 1, "name": "联系客服"}, {"id": 2, "name": "查看物流"}, {"id": 3, "name": "查看商品详情"}, {"id": 4, "name": "退款/退积分"}]
        actions_text = self.convert_actions_to_text(actions)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """你现在是喜马拉雅的客服机器人，你掌握熟练的用户沟通技巧，能通过结合订单信息、过往相关的其它用户的求助/投诉案例，给出很专业建议。帮当前用户解决在平台上遇到的一系列问题。
                """},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": chat_assistant_output},
                {"role": "user", "content": "请列一下动作列表"},
                {"role": "assistant", "content": actions_text},
                {"role": "user", "content": "请根据动作和当前求助/投诉的相关性，将‘动作列表’中的动作按照相关性从高到低排序，返回给我。直接返回动作的ID，不需要动作名称。用‘，’相隔。如：4,2,1,3"},
            ],
            temperature=0.1,
            max_tokens = 20,
        )
        summarized_text = response.choices[0].message.content
        print(response.usage)
        return summarized_text
    
    def convert_actions_to_text(self, actions):
        text = ""
        for i, action in enumerate(actions):
            text += f"动作ID：{action.get('id')}\n动作名称：{action.get('name')}\n\n"
        print(text)
        return text

# # 使用示例：
# action_assistant = ActionAssistant('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')
# output_text = action_assistant.query("商品一直未发货 要求退款", "亲，非常抱歉给您带来不便。根据您提供的订单信息，我们查询到了与您类似的案例，这些用户的订单也是长时间未发货，要求退款。我们建议您先联系卖家，了解一下商品的发货情况，如果卖家无法提供满意的解决方案，您可以在订单详情页申请退款，我们会尽快处理您的退款申请。同时，我们也会对卖家进行相应的处理，确保类似情况不再发生。")
# print(output_text)