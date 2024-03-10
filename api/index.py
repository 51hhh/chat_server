# -*- coding: UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import json
from urllib.parse import urlparse, parse_qs
import secrets
import supabase


# 数据库部分

import os
from supabase import create_client, Client

# 从环境变量获取这些值
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(url, key)



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
        if type_value == "sign_up":
            sign_up(self)
        elif type_value == "sign_in":
            sign_in(self)
        elif type_value == "message":
            message(self)
        elif type_value == "get_message":
            get_message(self)





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
            content_length = int(self.headers['Content-Length'])
            # 读取请求数据
            post_data = self.rfile.read(content_length)
            # 解析JSON数据
            post_data_json = json.loads(post_data.decode('utf-8'))
            # 返回解析后的JSON数据
            return post_data_json
        except:
            return None






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
    无 userid
    无 password
    用户已存在
"""


def sign_up(self): 

    # 解析JSON数据
    post_data_json = self.get_json()
    
    # 尝试解析json中的userid和token
    try:
        user_id_value = post_data_json['userid']
        password_value = post_data_json['password']

    except:
        self._send_error_response("无 userid或password包含在json内" ,status_code=400)


    # 检查是否为空值
    if user_id_value is None:
        self._send_error_response("userid为空" ,status_code=400)
        return
    if password_value is None:
        self._send_error_response("password为空", status_code=400)
        return



    # 使用Supabase数据库查询是否已有该userid
    try:
        data_exists = supabase.table("users").select("userid").eq("userid", user_id_value).execute()
    except:
        self._send_error_response("网络错误" ,status_code=404)
        return
    


    # 判断已有userid的列表是否为空
    # 就是是否有重复的id
    if data_exists.data:
        self._send_error_response(f"{user_id_value}已存在" ,status_code=400)

    else:
        new_user = {"userid": user_id_value, "password": password_value}
        # 在数据库中创建新用户
        try:
            supabase.table("users").insert(new_user).execute()
        
        except:
            self._send_error_response("网络错误" ,status_code=404)
            return
        
        # 用户成功创建，成功响应代码...
        data = {
            "user_id": user_id_value,
            "type": "sign_up",
            "message": "注册成功"
        }
        self._send_success_response(data, status_code=200)





"""
作用:
    使用给定的查询参数对用户进行登录操作。

参数:
    query_params (dict): 包含查询参数的字典。

返回:
    None
"""



# 登录函数
def sign_in(self): 

    # 解析JSON数据
    post_data_json = self.get_json()
    
    # 尝试解析json中的userid和token
    try:
        user_id_value = post_data_json['userid']
        password_value = post_data_json['password']

    except:
        self._send_error_response("无 userid或password包含在json内" ,status_code=400)


    # 检查是否为空值
    if user_id_value is None:
        self._send_error_response("userid为空" ,status_code=400)
        return
    if password_value is None:
        self._send_error_response("password为空", status_code=400)
        return

    
    # 查询用户
    try:
        user_info = supabase.table("users").select("*").eq("userid", user_id_value).execute()
    except:
        self._send_error_response("网络错误" ,status_code=404)
        return
    
    if user_info.data:
        user_info_data = user_info.data[0]
        # 对比密码
        if user_info_data["password"] == password_value:
            # 查询 token

            token = user_info.data[0]["token"]
            if token != None:
                # 用户已经登录的响应......
                # 发送带有 token 的登录成功响应......

                data = {
                    "user_id": user_id_value,
                    "type": "sign_in",
                    "message": "登录成功",
                    "token": token
                }
                self._send_success_response(data, status_code=200)

            else:
                # 生成token
                token = secrets.token_hex(16)
                
                try:
                    supabase.table("users").update({"token": token}).eq("userid", user_id_value).execute()
                except:
                    self._send_error_response("网络错误" ,status_code=404)
                    return

                # 发送带有 token 的登录成功响应......      
                data = {
                    "user_id": user_id_value,
                    "type": "sign_in",
                    "message": "登录成功,已成功生成token",
                    "token": token
                }
                self._send_success_response(data, status_code=200)
        else:
            self._send_error_response("密码错误" ,status_code=400)
    else:
        self._send_error_response(f"没有找到{user_id_value}的用户" ,status_code=400)







def message(self):
    print(f"Received POST request for {self.path}")


    # 解析JSON数据
    post_data_json = self.get_json()
    
    # 尝试解析json中的userid和token
    try:
        user_id_value = post_data_json['userid']
        token = post_data_json['token']
        message = post_data_json['message']

    except:
        self._send_error_response("无 userid,token或message包含在json内" ,status_code=400)


    # 检查是否为空值
    if user_id_value is None:
        self._send_error_response("userid为空" ,status_code=400)
        return
    if token is None:
        self._send_error_response("token为空", status_code=400)
        return
    if message is None:
        self._send_error_response("message为空", status_code=400)
        return
    

    # 数据库获取信息
    try:
        user_info = supabase.table("users").select("*").eq("userid", user_id_value).execute()
    except:
        self._send_error_response("网络错误" ,status_code=404)
        return
    
    # 将用户 ID、消息和时间戳整合
    # 获取当前时间并格式化
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        "userid": user_id_value,
        "message": message,
        "timestamp": now
    }

    
    # 鉴权
    if user_info.data:
        user_info_data = user_info.data[0]
        if token == user_info_data["token"]:
        
            try:
                supabase.table("messages").insert(message_data).execute()
            except:
                self._send_error_response("网络错误" ,status_code=404)
                return
            
            # 如果保存成功，发送成功响应
            data = {
                "message": "消息发送成功",
                "timestamp": now
            }
            self._send_success_response(data, status_code=200)
            
        else:
            self._send_error_response("token错误" ,status_code=400)
    else:
        self._send_error_response(f"没有找到{user_id_value}的用户" ,status_code=400)








def get_message(self):

    # 解析JSON数据
    post_data_json = self.get_json()
    

    # 尝试解析json中的userid和token
    try:
        user_id_value = post_data_json['userid']
        token = post_data_json['token']
    except:
        self._send_error_response("无 userid或者token包含在json内" ,status_code=400)


    # 检查是否为空值
    if user_id_value is None:
        self._send_error_response("userid为空" ,status_code=400)
        return
    elif token is None:
        self._send_error_response("token为空" ,status_code=400)
        return


    try:
        user_info = supabase.table("users").select("*").eq("userid", user_id_value).execute()
    except:
        self._send_error_response("网络错误" ,status_code=404)
        return


    if user_info.data:
        user_info_data = user_info.data[0]
        if token == user_info_data["token"]:
        
            
            try:
                chat_history_response = supabase.table("messages").select("*").execute()
            except:
                self._send_error_response("网络错误" ,status_code=404)
                return
             # 发送聊天历史的json字符串
            chat_history_data = chat_history_response.data
            self._send_success_response(chat_history_data, status_code=200)
        else:
            self._send_error_response("token错误" ,status_code=400)
    else:
        self._send_error_response(f"没有找到{user_id_value}的用户" ,status_code=400)


       






def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting chat server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
