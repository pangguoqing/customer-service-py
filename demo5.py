import csv
import re

with open('demo5.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # 读取表头

    processed_data = []  # 用于存储处理后的数据
    for row in reader:
        row0 = row[0]  # 提取咨询单内容
        row0 = re.sub(r"\s+", '', row0)  # 去除空白
        row0 = re.sub(r'所属供应商名称：\$.+?\$', '', row0)  # 去除供应商相关信息
        row0 = re.sub(r'(用户ID|订单编号|同咨询单|用户诉求|订单ID|订单号|物流单号)[:：]', '', row0)
        row0 = re.sub(r'[a-zA-Z0-9_-]{7,}', '', row0)  # 去数字字母混合字符串
        row0 = re.sub(r'^[，。！？：,.!?:]+', '', row0) # 去除开头的特定符号
        
        row1 = row[1]
        row1 = re.sub(r"\s+", '', row1)  # 去除空白
        row1 = re.sub(r'是否解决：.+', '', row1)  # 去除是否解决
        row1 = re.sub(r'(用户未提供|未提供 已解决|已解决|未提供|未回复离线)', '', row1)
        row1 = re.sub(r'提供方案[:：]', '', row1)  # 去除“提供方案：”
        row1 = re.sub(r'^[，。！？：,.!?:]+', '', row1) # 去除开头的特定符号

        processed_row = [row1] 
        processed_row = [row0] + [row1] + [row[2]] 
        processed_data.append(processed_row)
        # # row是一个列表，包含CSV文件中的一行数据
        # # 可以根据需要对每一行进行处理
        # if row[5] != '直接关单':
        #     processed_data.append(row[5])  # 将符合条件的数据添加到列表中

# 保存处理后的数据到另一个CSV文件
with open('demo5_output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(header)  # 写入表头
    writer.writerows(processed_data)  # 写入处理后的数据
