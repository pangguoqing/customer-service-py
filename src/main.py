from chat_assistant import ChatAssistant
from action_assistant import ActionAssistant
import time

api_key = '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'

t = time.time()
chat_assistant = ChatAssistant(api_key, './embeddings.csv')
# print('main_1', time.time() - t)
action_assistant = ActionAssistant(api_key)
# print('main_2', time.time() - t)

user_input = "迪奥口红是正品吗？"
print("用户求助/投诉: ", user_input)

chat_output_text = chat_assistant.query(user_input, {
    "id": "xm10000001",
    "product": "迪奥口红",
    "at": "20230514 22:00:00"
})
# print('main_3', time.time() - t)
action_output_text = action_assistant.query(user_input, chat_output_text)
# print('main_4', time.time() - t)

print("AI_回复: ", chat_output_text)
print("AI_推荐: ", action_output_text)
