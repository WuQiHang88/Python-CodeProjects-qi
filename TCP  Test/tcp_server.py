import socket
#服务端的编写
def run_server():
    #创建一个TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #设置服务器地址和部门
    server_address = ('localhost', 8888)

    #绑定地址和端口（这是因为套接字由IP地址与端口组成，其中localhost表示本地主机）
    server_socket.bind(server_address)

    # 监听（即指服务器准备好接收客户端连接的一个状态，类似于一个开门营业的状态）连接，参数1表示允许的最大连接队列长度
    # 在监听前，需要需要把套接字绑定到一个明确的 IP 地址和端口上。比如('localhost', 8888)，这样客户端才能知道往哪里发送连接请求。
    server_socket.listen(1)
    print(f"服务器正在监听{server_address[0]} : {server_address[1]}...")

    while True:  #创建一个无限循环，使服务器可以持续接收多个客户端连接
        # 等待客户端连接
        print("等待客户端连接。。。")
        # accept()方法会阻塞程序，直到有客户端连接到来。
        # 返回一个新的客户端套接字client_socket和客户端地址client_address。
        # 服务器套接字server_socket继续监听新连接，而client_socket用于与当前客户端通信
        client_socket, client_address = server_socket.accept()

        try:
            print(f"客户端:{client_address} 已连接")
            # 接收客户端信息，最多读取1024字节
            data = client_socket.recv(1024)
            #将数据解析为UTF-8字符串并打印
            print(f"收到消息:{data.decode('utf-8')}")

            #发送响应给客户端
            response = "你好，客户端！我已收到你的消息。"
            #同理，将响应信息编码为 UTF-8 字节流并发送给客户端
            client_socket.sendall(response.encode('utf-8'))
            print("响应已发送")

        finally:
            # 关闭连接
            client_socket.close()
            print("客户端连接已关闭")

if __name__ == "__main__":
    run_server()

# 工作逻辑如下：
# 服务器创建套接字并绑定到指定地址和端口。
# 服务器开始监听客户端连接。
# 当客户端连接到来时，服务器接受连接并创建新的套接字用于通信。
# 服务器接收客户端消息，处理后发送响应。
# 通信结束后，关闭与客户端的连接，但服务器继续监听新连接