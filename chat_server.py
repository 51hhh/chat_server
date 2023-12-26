# -*- coding: UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import json

# 存储聊天信息的列表
chat_history = []

class ChatServer(BaseHTTPRequestHandler):

    """
    该函数处理GET请求。

    它记录请求信息，并发送一个带有聊天历史的JSON格式响应。

    参数:
        self: 类的实例。

    返回:
        无
    """
    def do_GET(self):
        # 记录请求信息
        print(f"Received GET request for {self.path}")

        # 发送响应状态码
        self.send_response(200)
        # 设置响应头部为json格式
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        # 发送聊天历史的json字符串
        chat_history_json = json.dumps(chat_history)
        self.wfile.write(chat_history_json.encode('utf-8'))

        # 显示返回值
        print(f"  Sent response with chat history.\n")

    """
    处理POST请求。

    记录请求信息。
    获取并解析请求数据。
    检查请求数据中是否包含'userId'和'message'。
    从请求数据中提取'userId'和'message'。
    将用户ID、消息和时间戳存储到聊天历史记录中。
    发送状态码为200的响应，并设置响应头部为纯文本格式。
    向响应正文写入确认消息。
    """
    def do_POST(self):
        # 记录请求信息
        print(f"Received POST request for {self.path}")

        # 获取请求内容长度
        content_length = int(self.headers['Content-Length'])
        # 读取请求数据
        post_data = self.rfile.read(content_length)
        # 解析JSON数据
        post_data_json = json.loads(post_data.decode('utf-8'))

        # 检查是否有 userId
        if 'userId' not in post_data_json:
            self._send_error_response("无 userId")
            return

        # 检查是否有 message
        if 'message' not in post_data_json:
            self._send_error_response("无 message", status_code=400)
            return

        # 提取 userId 和 message
        user_id = post_data_json['userId']
        message = post_data_json['message']

        # 获取当前时间并格式化
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 将用户 ID、消息和时间存储到聊天历史列表中
        chat_history.append({"userId": user_id, "message": message, "timestamp": now})

        # 发送响应状态码
        self.send_response(200)
        # 设置响应头部为纯文本格式
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        # 发送确认信息
        response_message = f"Message from user {user_id} received at {now}"
        self.wfile.write(response_message.encode('utf-8'))

        # 显示返回值
        print(f"Sent response: {response_message}")

    def _send_error_response(self, error_message, status_code=400):
        # 发送错误响应状态码
        self.send_response(status_code)
        # 设置响应头部为纯文本格式
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        # 发送错误信息
        self.wfile.write(error_message.encode('utf-8'))

        # 显示返回值
        print(f"Sent error response: {error_message}")
def run(server_class=HTTPServer, handler_class=ChatServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting chat server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
