import csv
import re

with open('demo4.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # 读取表头

    processed_data = []  # 用于存储处理后的数据
    for row in reader:
        if row[6] == '在线' and row[5] != '电话' and row[5] != '私信' and row[4] != '-':
            row3 = row[3]  # 提取咨询单内容
            row3 = re.sub(r'用户ID：\d+', '', row3)  # 去除用户ID相关信息
            row3 = re.sub(r'所属供应商名称：\$.+?\$', '', row3)  # 去除供应商相关信息
            row3 = re.sub(r'订单编号：\n\d+', '', row3)  # 去除订单ID
            row3 = re.sub(r'同咨询单：\n\d+', '', row3)  # 去除同咨询单
            row3 = re.sub(r'用户诉求：', '', row3)  # 去除“用户诉求：”

            # 去除多余的空格和换行符
            row3 = row3.strip().replace('\n', ' ').replace('\r', '')
            if row3.startswith(("，", "。", "！", "？", "：", ",", ".", "!", "?", ":")):
                row3 = row3[1:]  # 去除开头符号
                
            row4 = row[4]
            # 去除问题解决信息
            row4 = re.sub(r'是否解决：.+', '', row4)  # 去除是否解决
            # 去除问题解决信息
            row4 = re.sub(r'(用户未提供|未提供 已解决|已解决|未提供|未回复离线)', '', row4)
            row4 = re.sub(r'提供方案：', '', row4)  # 去除“提供方案：”

            # 去除多余的空格和换行符
            row4 = row4.strip().replace('\n', ' ').replace('\r', '')

            if row4.startswith(("，", "。", "！", "？", "：", ",", ".", "!", "?", ":")):
                row4 = row4[1:]  # 去除开头符号
                
            # processed_row = [row3] + row[0:3] + row[4:]
            processed_row = [row4] 
            # processed_row = [row3] + [row[4]] 
            processed_data.append(processed_row)
            # # row是一个列表，包含CSV文件中的一行数据
            # # 可以根据需要对每一行进行处理
            # if row[5] != '直接关单':
            #     processed_data.append(row[5])  # 将符合条件的数据添加到列表中

# 保存处理后的数据到另一个CSV文件
with open('demo4_output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # 写入表头
    writer.writerows(processed_data)  # 写入处理后的数据
