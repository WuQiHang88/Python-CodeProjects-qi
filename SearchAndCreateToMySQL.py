import mysql.connector
from mysql.connector import Error

# 数据库配置
config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'wuqi810742777',
    'database' : 'sys'
}

try:
    #连接数据库
    conn = mysql.connector.connect(**config)

    if conn.is_connected():
        print("成功连接到数据库")

        #创建游标对象
        cursor = conn.cursor()

        # 1. 查询数据库
        query = "SELECT * FROM sys_config"
        cursor.execute(query)
        records = cursor.fetchall()

        print("\n查询结果：")
        for row in records:
            print(row)

        # 2.插入数据
        insert_query = """
            INSERT INTO sys_config (variable, value, set_time)
            VALUES (%s, %s, %s)
            """  # 前面的sys_config表示你要插入的表名，后面为这个表的字段，这些都是需要一一对应的
        # 显式插入三个字段（第四个字段id自增）

        # 准备数据（三个值的元组，对应占位符顺序）
        data = (
            'wangxiaoming@example.com',
            '666',
            '2025-05-19 14:30:00'  #在这个data里，按照上面定义的数据，一一对应的写下要插入的信息 # 手动指定时间戳（若需使用默认值则删除此字段和占位符）
        )

        cursor.execute(insert_query, data)
        conn.commit()
        print(f"插入成功，新记录ID: {cursor.lastrowid}")  # 获取自增ID

        # 3.同时修改多个字段的内容
        update_query = """
        UPDATE sys_config 
        SET 
            variable = %s,
            set_time = %s
        WHERE value = %s
        """   #前面的sys_config是表名，后面set是要修改的字段（这个表里面的字段），where是用来定位的（可以和MySQL里的筛选代码类比）

        data = (
            '915866@qq.com', #对应variable
            '2000-05-19 14:30:00', #对应set_time
            "64"  #对应where的筛选
        )

        cursor.execute(update_query, data)
        conn.commit()
        print(f"修改成功，影响行数: {cursor.rowcount}")

except Error as e:
    print(f"数据库错误: {e}")