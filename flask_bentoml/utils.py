import random
import string

import pymysql


def key_generate(length=10, include_upper=True, include_lower=True, include_digits=True):
    """
    生成一个随机字符串。

    参数:
    length (int): 生成的字符串长度。
    include_upper (bool): 是否包含大写字母。
    include_lower (bool): 是否包含小写字母。
    include_digits (bool): 是否包含数字。

    返回:
    str: 一个随机生成的字符串。
    """
    # 定义字符集
    characters = ""
    if include_upper:
        characters += string.ascii_uppercase
    if include_lower:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits

        # 确保至少有一个字符集被选中
    if not characters:
        raise ValueError("至少需要选择一个字符集（大写字母、小写字母或数字）。")

        # 生成随机字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

# 连接数据库
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='flask_service', port=3306,
                       charset='utf8')
cursor = conn.cursor()


# 获取API对应的key值
def get_key(api):
    try:
        sql = "select key_ from api_key where api='%s';" % (api)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print(e)
        conn.rollback()

