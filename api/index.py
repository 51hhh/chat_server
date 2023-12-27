# -*- coding: UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import json
from urllib.parse import urlparse, parse_qs
import secrets
# 存储聊天信息的列表
chat_history = []
userID_list = []
usertoken_list = []

class handler(BaseHTTPRequestHandler):

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
        self.send_header('Access-Control-Allow-Origin', '*')#设置允许跨域
        self.send_header('Content-type', 'application/json')#设置响应格式
        self.end_headers()#结束响应
        # 发送聊天历史的json字符串
        self.wfile.write(json.dumps(chat_history).encode('utf-8'))


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
        path = self.path#获取请求路径
        parsed_url = urlparse(path)#urlparse(url) 解析整个URL，并返回一个包含其各个组成部分的 ParseResult 对象。
        query_params = parse_qs(parsed_url.query)#parse_qs(parsed_url.query) 将查询字符串 parsed_url.query 转换为一个字典，其中字典的键是查询参数的名称，值是参数值的列表。
        type_value = query_params.get('type', [None])[0] #尝试从查询参数字典中获取 type 键的值。如果没有该键，则返回一个包含 None 的列表，并从中取出第一个元素。由于每个键都对应一个值的列表，即使只有一个值，我们也需要通过索引 [0] 获取它。
        if type_value == "sign_up":
            sign_up(self,query_params)
        elif type_value == "sign_in":
            sign_in(self,query_params)
        elif type_value == "message":
            message(self,query_params)
















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





"""
使用给定的查询参数注册用户。
作用:
    在服务器上注册新用户。

参数:
    self: 
    query_params (dict): 包含查询参数的字典。

返回:
    None

异常:
    None

异常处理:
    无 userId
    无 password
    用户已存在
"""


def sign_up(self,query_params): 

    user_id_value = query_params.get('userId', [None])[0] 
    password_value = query_params.get('password', [None])[0]


    # 读取此userId的登陆状态
    users_a_info= [item for item in userID_list if item["userId"] == user_id_value]


    if user_id_value is None:
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            "user_id": "",
            "type": "sign_up",
            "message": "无 userId"
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))
        print(f"注册失败,无 userId")
        return
    elif password_value is None:
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            "user_id": user_id_value,
            "type": "sign_up",
            "message": "无 password"
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))
        print(f"注册失败，无 password")
        return
    

    # 判断已有userid的列表是否为空
    # 就是是否有重复的id
    elif users_a_info:
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            "user_id": user_id_value,
            "type": "sign_up",
            "message": "用户已存在"
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))
        print(f"注册失败，用户名为 {user_id_value} 的用户已存在")


    else:
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            "user_id": user_id_value,
            "type": "sign_up",
            "message": "注册成功"
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))
        print(f"注册成功")


        userID_list.append({"userId": user_id_value, "password": password_value})



"""
作用:
    使用给定的查询参数对用户进行登录操作。

参数:
    query_params (dict): 包含查询参数的字典。

返回:
    None
"""

def sign_in(self,query_params):
    # 获取post传入的 userId 和 password 的值
    user_id_value = query_params.get('userId', [None])[0] 
    password_value = query_params.get('password', [None])[0]
    
    if user_id_value is None:
        self.send_response(201)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = {
            "user_id": "",
            "type": "sign_in",
            "message": "无 userId"
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))
        print(f"登录失败，无 userId")
        return
    else:
        users_a_info = [item for item in userID_list if item["userId"] == user_id_value]
        if users_a_info:
            for user_info in users_a_info:
                print(f"找到了用户 {user_id_value}，密码是:", user_info["password"])
                
                if user_info["password"] == password_value:
                    # 密码通过


                    # 读取此userId的登陆状态
                    users_a_token= [item for item in usertoken_list if item["userId"] == user_id_value]
                    # 判断返回的列表是否为空
                    if users_a_token:
                        for users_token in users_a_token:
                            print(f"找到了用户 {user_id_value}，token是:")
                            #user是否已经有token
                            print(f"用户 {user_id_value} 已登录，无需重复登录")

                            token = users_token["token"]

                            self.send_response(201)
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            data = {
                                "user_id": user_id_value,
                                "type": "sign_in",
                                "message": "已登录，无需重复登录",
                                "token": token
                            }
                            self.wfile.write(json.dumps(data).encode('utf-8'))
                            return
                    else:

                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()

                        token = secrets.token_hex(16)
                        usertoken_list.append({"userId": user_id_value, "token": token})

                        data = {
                            "user_id": user_id_value,
                            "type": "sign_in",
                            "message": "登录成功",
                            "token": token
                        }
                        self.wfile.write(json.dumps(data).encode('utf-8'))
                        print(f"登录成功")
                        return
                    


                else:
                    self.send_response(201)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    data = {
                        "user_id": user_id_value,
                        "type": "sign_in",
                        "message": "密码错误"
                    }
                    self.wfile.write(json.dumps(data).encode('utf-8'))
                    print(f"登录失败，密码错误")
                    return


        else:
            print("没有找到用户 ", user_id_value)
            self.send_response(201)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = {
                "user_id": "",
                "type": "sign_in",
                "message": "用户不存在"
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            print(f"登录失败，用户不存在")
            return


def message(self,query_params):
    print(f"Received POST request for {self.path}")

    # 获取请求内容长度
    content_length = int(self.headers['Content-Length'])
    # 读取请求数据
    post_data = self.rfile.read(content_length)
    # 解析JSON数据
    post_data_json = json.loads(post_data.decode('utf-8'))

    # 检查是否有 userId
    if 'userId' not in post_data_json:
        self._send_error_response("无 userId" ,status_code=201)
        return

    # 检查是否有 message
    if 'message' not in post_data_json:
        self._send_error_response("无 message", status_code=201)
        return
    
    if 'token' not in post_data_json:
        self._send_error_response("无 token", status_code=201)
        return
    
    user_id = post_data_json['userId']
    user_token = post_data_json['token']
    message = post_data_json['message']


    users_a_info= [item for item in usertoken_list if item["userId"] == user_id]
    if users_a_info:
        for user_info in users_a_info:
            print(f"找到了用户 {user_id}，token是:", user_info["token"])
            if user_info["token"] == user_token:
                # 获取当前时间并格式化
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 将用户 ID、消息和时间存储到聊天历史列表中
                chat_history.append({"userId": user_id, "message": message, "timestamp": now})
                
                # 发送响应
                data = {
                    "user_id": user_id,
                    "message": f"{message}发送成功",
                    "time": now
                }

                self.send_response(200)# 发送响应状态码
                self.send_header('Access-Control-Allow-Origin', '*')    #设置响应头以允许跨域请求。星号 * 表示接受任何域的请求。
                self.send_header('Content-type', 'application/json')    # 设置响应头部为json格式
                self.end_headers()# 结束 HTTP 头部的发送。
                self.wfile.write(json.dumps(data).encode('utf-8'))  #转换为 JSON 字符串，并以 UTF-8 编码方式写入响应。
                print(f"发送成功")
                return
            else:
                data ={
                    "user_id": user_id,
                    "message": "token与用户名不匹配，请清除token重新登录"
                }
                self.send_response(201)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
                print(f"token与用户名不匹配，请清除token重新登录")
                return










def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting chat server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()

