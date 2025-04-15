import pandas as pd

#首先确认你已经安装且引入pandas库，如果没有，需打开power shell输入pip install pandas（手动下载）
#然后就是读取文件，pd为前面的定义名，。read_excel表示pandas的excel文件读取，然后就是excel文件本地路径（可修改），最后是openpyx1引擎（可按照不同的读取文件修改），就是专门来解析.xlsx文件的
df = pd.read_excel('/Users/LENOVO/Documents/旧时代的产物/666/建模比赛数据/2023美赛/79797979.xlsx',engine='openpyxl')
data = df.to_dict(orient='records')#df.to_dict（）将其转换为字典，orient='records'表示按行来生成字典，例如：输出案例 {'content': '文本1', 'category': '新闻'},


formatted_data = []#最终传出去的数据列表
for row in data:
    item = {
        "text": row['word'],#这个为第一行的第一列的文本
        "metadata":{
            "source":"excel",
            "1 try": row['1 try'],#其他为第一行的除第一列的文本
            "2 tries": row['2 tries'],
            "3 tries": row['3 tries'],
            "4 tries": row['4 tries'],
            "5 tries": row['5 tries'],
            "6 tries": row['6 tries'],
            "x tries": row['x tries'],
        }
    }
    formatted_data.append(item)

    print(item)


#下面为所有数据只输出一行
#formatted_data = []
#for row in data:
    #formatted_data.append({
        #"text": row['content'],
        #"metadata": {
            #"source": "excel",
            #"category1": row['category1'],
            #"category2": row['category2'],
            # ...其他字段
        #}
    #})

# 所有数据处理完成后，统一输出一次，注意缩进！！
#print(formatted_data)

