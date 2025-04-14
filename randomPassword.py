import argparse
import secrets
import string


def create_password(length=12):
    if length < 8:
        raise ValueError("密码最少为8位")

    #首先，设置各种参数，例如大小写，符号，数字等，通过string处理模块完成
    up = string.ascii_uppercase  # string 为内置字符串处理模块， ascii_uppercase 为预设的大写字母串
    low = string.ascii_lowercase  # 理由同上，但是为预设的小写字母
    symbols = string.punctuation  # 预设的符号
    digits = string.digits  # 预设的数字
    all_chars = up + low + symbols + digits
    #确定密码里最少应该包含什么
    password = [
        secrets.choice(up),
        secrets.choice(low),
        secrets.choice(symbols),
        secrets.choice(digits)
    ]

    other_length = length - 4  #即除去前面定义的，必须包含的四个元素外，其他密码的长度
    for _ in range(other_length):  # range为生成一个整数序列，_表示忽略循环变量值，即不关心不需要输出第几次循环
        password.append(secrets.choice(all_chars))  # 即passport里强制添加all_chars变量所包含的东西
    #注意for后面的缩进！！如果下面两个语句的缩进和password.append(secrets.choice(all_chars))一样，即表示下面两句包含在for循环里，所以这个点是需要注意的！！
    secrets.SystemRandom().shuffle(password)  # 前面为内置的安全的随机生成数，后面的. shuffle为随机打乱字符顺序
    return ''.join(password)  # 表示用空号符链接字符串


def main():
    parser = argparse.ArgumentParser(description="安全密码生成器") #description:定义名称+初始化命令行参数
    parser.add_argument('-l', '--length', type=int, default=12, help="密码长度最少8位")#（一个密码里有几个符号/数字/字母）其中-l:短参数名（方便后面运行脚本时输入），type=int:长参数名，default=12默认密码长度为12
    parser.add_argument('-n', '--number', type=int, default=1, help="生成密码数量")#（一共生成多少条代码）-n为短参数名（同上），--number为长参数名，default为默认生成一条代码
    args = parser.parse_args()#将用户输入的命令行参数转换为对象属性
#即整个逻辑如下，用户运行脚本→输入参数→-l密码长度，-n设置生成数量→无参数即表示使用默认值→生成密码

    if args.length < 8:
        parser.error("密码长度至少为8位")

    for _ in range(args.number):
        print(create_password(args.length))


if __name__ == '__main__':  #判断模块是否直接运行，如果是则执行main函数
    main()


# 如何运行本脚本？用cmd（即打开powershell），进入到脚本所在文件夹，如何输入python randomPassword.py（这个即表示无参数直接运行脚本），python randomPassword.py -l 15 -n 2（即表示运行这个脚本的同时，输入相关参数，-l和-n为提前预定的参数，表示长度和密码数量）