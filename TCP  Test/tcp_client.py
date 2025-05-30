import socket
#客户端的编写
def run_client():
    #创建一个TCP/IP套接字（套接字是由IP地址和端口号组合而成的一个标识符，可以理解为IP地址的作用是确定网络中设备，端口号是区分同个设备的不同应用程序）
    #套接字相当于两个程序间进行通讯的“接口”或“门口”
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #socket.AF_INET表明使用IPv4地址族，socket.SOCK_STREAM表示使用面向连接的TCP协议

    #设置服务器地址和端口（设定服务器的地址为本地地址localhost（即ip）端口号为8888）
    server_address = ('localhost', 8888)

    # 连接服务器
    print(f"正在连接{server_address[0]}:{server_address[1]}...")
    #让客户端套接字尝试连接到指定的服务器地址和端口
    client_socket.connect(server_address)

    try:
        # 发送信息给服务器
        message = "你好，服务器！这是客户端发送的信息。"
        #把消息编码成utf-8，然后通过套接字发送给服务器，sendall方法保证数据全部发送
        client_socket.sendall(message.encode('utf-8'))
        print("消息已发送")

        #接收服务器响应
        #从套接字接收服务器返回的数据，最多接收1024字节
        data = client_socket.recv(1024)
        print(f"收到响应:{data.decode(('utf-8'))}")

    finally:
        # 关闭客户端套接字，终止与服务器的连接
        client_socket.close()
        print("连接已关闭")


if __name__ == "__main__":
    run_client()



