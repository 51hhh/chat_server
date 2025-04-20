# -*- coding: UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

# 导入
from operation import *



class handler(BaseHTTPRequestHandler):

    """
    处理POST请求。

    记录请求信息。
    获取并解析请求数据。
    检查请求数据中是否包含'userid'和'message'。
    从请求数据中提取'userid'和'message'。
    将用户ID、消息和时间戳存储到聊天历史记录中。
    发送状态码为200的响应，并设置响应头部为纯文本格式。
    向响应正文写入确认消息。
    """
    def do_POST(self):
        path = self.path#获取请求路径
        parsed_url = urlparse(path)#urlparse(url) 解析整个URL，并返回一个包含其各个组成部分的 ParseResult 对象。
        query_params = parse_qs(parsed_url.query)#parse_qs(parsed_url.query) 将查询字符串 parsed_url.query 转换为一个字典，其中字典的键是查询参数的名称，值是参数值的列表。
        type_value = query_params.get('type', [None])[0] #尝试从查询参数字典中获取 type 键的值。如果没有该键，则返回一个包含 None 的列表，并从中取出第一个元素。由于每个键都对应一个值的列表，即使只有一个值，我们也需要通过索引 [0] 获取它。
        
        # 解析JSON数据
        # post_data_json的json长度只计算一次，调用self.get_json()将完成计算，故一次请求只能解析一次。
        post_data_json = self.get_json()
        if type_value == "sign_up":
            sign_up(self,post_data_json)
        elif type_value == "sign_in":
            sign_in(self,post_data_json)

        # 鉴权
        elif (check_user_token(self,post_data_json)==True):
            if type_value == "message":
                message(self,post_data_json)
            elif type_value == "get_message":
                get_message(self,post_data_json)
            elif type_value == "apply_for":
                apply_for(self,post_data_json)
            elif type_value == "agree":
                agree(self,post_data_json)
            elif type_value == "get_apply":
                get_apply(self,post_data_json)
            elif type_value == "create_group":
                create_group(self,post_data_json)
            elif type_value == "get_group":
                get_group(self,post_data_json)
            elif type_value == "search_group":
                search_group(self,post_data_json)





    def _send_error_response(self, error_message, status_code=400):
        # 发送错误响应状态码
        self.send_response(status_code)
        # 设置响应头部为纯文本格式
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        # 发送错误信息
        self.wfile.write(error_message.encode('utf-8'))

        # 显示返回值
        print(f"Sent error response: {error_message}")


    def _send_success_response(self, data, status_code=200):
        # 发送成功响应状态码
        self.send_response(status_code)
        # 设置响应头部为纯文本格式
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # 发送成功信息
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def get_json(self):
        try:
            # 获取请求内容长度
            # Content-Length Header 是为了向服务器表明这个请求的 Body 的大小。服务器使用这个值来准确解析请求的 Body。
            content_length = int(self.headers['Content-Length'])
            # 读取请求数据
            post_data = self.rfile.read(content_length)
            # 解析JSON数据
            post_data_json = json.loads(post_data.decode('utf-8'))
            # 返回解析后的JSON数据
            return post_data_json
        except:
            return None




def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting chat server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
