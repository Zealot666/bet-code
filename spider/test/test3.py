import json

# 文件
finename = r"C:\Users\c\Desktop\ip.txt"

f = open(finename,encoding='utf-8')  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法

while line:
    # 在Python3中使用
    print(line, end='')
    # 如果每行是json的字符串形式
    # line_json = json.loads(line)
    # filename = line_json["filename"])
    # content = line_json["parse_text"])

f.close()