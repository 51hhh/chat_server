# -*- coding: UTF-8 -*-
from datetime import datetime
import secrets
import supabase
import re


# 数据库部分

import os
from supabase import create_client, Client

# 全局缓存，存储最近的消息数据
MESSAGES_CACHE = []
USERS_INFO = []
GROUP_MEMBERS = []
GROUPS_INFO = []


# 从环境变量获取这些值
url: str = os.environ.get("SUPABASE_URL")

key: str = os.environ.get("SUPABASE_KEY")




# 初始化

supabase: Client = create_client(url, key)


# 获取users库内容缓存至USERS_INFO
def get_user_info(self,user_id):
    global USERS_INFO
    if USERS_INFO == []:
        try:
            history_user_info = supabase.table("users").select("*").execute()
        except:
            self._send_error_response("网络错误，连接数据库失败" ,status_code=404)
            a_user_info = {}
            return a_user_info
        # 本地缓存
        USERS_INFO = history_user_info.data
        a_user_info = [message for message in USERS_INFO if message['userid'] == user_id]
        return a_user_info
    else:
        # 从缓存中获取信息
        a_user_info = [message for message in USERS_INFO if message['userid'] == user_id]
        return a_user_info

def get_group_members(self,user_id,group_id=None):
    global GROUP_MEMBERS
    if GROUP_MEMBERS == []:
        try:
            history_group_members = supabase.table("groupmembers").select("*").execute()
        except:
            self._send_error_response("网络错误" ,status_code=404)
            return
        # 本地缓存
        GROUP_MEMBERS = history_group_members.data

    # 若group_id为all，返回所有群组  
    if group_id == None:
        a_user_in_group = [message for message in GROUP_MEMBERS if message['userid'] == user_id]
        return a_user_in_group
    elif group_id == 'all':
        return GROUP_MEMBERS



# 获取表groups库内容缓存至GROUPS_INFO
def get_group_list(self):
    global GROUPS_INFO
    if GROUPS_INFO == []:
        try:
            history_GROUPS_INFO = supabase.table("groups").select("*").execute()
        except:
            self._send_error_response("网络错误" ,status_code=404)
            return
        # 本地缓存
        GROUPS_INFO = history_GROUPS_INFO.data
        return GROUPS_INFO
    else:
        # 从缓存中获取信息
        return GROUPS_INFO





## 检查user与token匹配情况
def check_user_token(self,post_data_json):
    # 尝试解析json中的userid和token
    try:
        user_id_value = post_data_json['userid']
        token = post_data_json['token']

    except:
        self._send_error_response("无 userid或token包含在json内" ,status_code=400)


    # 检查是否为空值
    if user_id_value is None:
        self._send_error_response("userid为空" ,status_code=400)
        return False
    if token is None:
        self._send_error_response("token为空", status_code=400)
        return False



    # 返回匹配userid的所有信息[{'userid': '123456', 'password': '123456', 'token': '96e0f5b8b2c5c88dd6134b4cabae2734', 'token_time': None}]
    a_user_info = get_user_info(self,user_id_value)
    
    # 若为空则无此用户，判断长度是否非零
    if len(a_user_info) != 0:
        # 获取用户信息字典
        user_info_dict = a_user_info[0]
        #对比token
        if token == user_info_dict.get("token",None):
            return True
        else:
            self._send_error_response("token错误" ,status_code=400)
            return False
    else:
        self._send_error_response(f"没有找到{user_id_value}的用户" ,status_code=400)
        return False

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



def sign_up(self,post_data_json):     
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
def sign_in(self,post_data_json): 
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
            
            # 用户登录，清除本地用户缓存USERS_INFO以确保token被真确加载
            global USERS_INFO
            USERS_INFO = []
            
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







def message(self,post_data_json):
    print(f"Received POST request for {self.path}")

    # 解析JSON数据
    post_data_json = post_data_json
    
    # 尝试解析json中的userid和token
    try:
        user_id_value = post_data_json['userid']
        message = post_data_json['message']
        group_id = post_data_json['group_id']

    except:
        self._send_error_response("无 userid,token或message包含在json内" ,status_code=400)


    # 检查是否为空值
    if message is None:
        self._send_error_response("message为空", status_code=400)
        return
    

    # 将用户 ID、消息和时间戳整合
    # 获取当前时间并格式化
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        "userid": user_id_value,
        "message": message,
        "timestamp": now,
        "group_id": group_id
    }

       
    try:
        supabase.table("messages").insert(message_data).execute()
    except:
        self._send_error_response("网络错误" ,status_code=404)
        return
    
    # 清除本地消息缓存
    global MESSAGES_CACHE
    MESSAGES_CACHE = []

    # 如果保存成功，发送成功响应
    data = {
        "message": "消息发送成功",
        "timestamp": now
    }
    self._send_success_response(data, status_code=200)
    






def get_message(self,post_data_json):
    print(f"Received POST request for {self.path}")
    
    # 尝试解析json中的userid和token
    try:
        user_id = post_data_json['userid']
        group_id = post_data_json['group_id']
    except:
        self._send_error_response("无 group_id包含在json内" ,status_code=400)
        return

    # 检查是否为空值
    if group_id is None:
        self._send_error_response("group_id为空", status_code=400)
        return
    
    # 公共群聊
    if group_id == "1":
        print("public_group")
    else:
        # 检查用户在群聊中权限
        a_user_in_group = get_group_members(self,user_id)
        a_user_in_group = [message for message in a_user_in_group if message['group_id'] == group_id]

        # 若为空则不在群内，判断长度是否非零
        
        if len(a_user_in_group) != 0:
            print(a_user_in_group)
        else:
            self._send_error_response(f"{user_id}的用户不在{group_id}群内" ,status_code=400)
            return 
    

    # 如果有缓存
    global MESSAGES_CACHE
    if MESSAGES_CACHE == []:
        try:
            chat_history_response = supabase.table("messages").select("*").execute()
        except:
            self._send_error_response("网络错误" ,status_code=404)
            return
        # 本地缓存
        MESSAGES_CACHE = chat_history_response.data
    else:
        # 从缓存中获取信息
        MESSAGES_CACHE = MESSAGES_CACHE

    messages_in_group = [message for message in MESSAGES_CACHE if message['group_id'] == group_id]
    self._send_success_response(messages_in_group, status_code=200)


       

def apply_for(self,post_data_json):
    # 尝试解析json中的userid和token
    try:
        user_id = post_data_json['userid']
        group_id = post_data_json['group_id']
    except:
        self._send_error_response("无 user_id或group_id包含在json内" ,status_code=400)
        return

    # 检查是否为空值
    if group_id is None:
        self._send_error_response("group_id为空", status_code=400)
        return
    if user_id is None:
        self._send_error_response("user_id为空", status_code=400)
        return
    
    # 检测此群是否存在
    group_list = get_group_list(self)
    group_list = [message for message in group_list if message['group_id'] == group_id]
    if len(group_list) == 0:
        self._send_error_response(f"申请无效，群ID{group_id}非法" ,status_code=400)
        return
    
    # 是否已经在群内
    a_user_in_group = get_group_members(self,user_id)
    # 检测是否已经进入群聊
    user_in_group = [message for message in a_user_in_group if message['group_id'] == group_id]
    # 检测是否已经位于群聊申请列表
    user_in_add_group = [message for message in a_user_in_group if message['add_group_id'] == group_id]
    if len(user_in_group) == 0:
        if len(user_in_add_group) == 0:
            members_data = {
                "userid": user_id,
                "add_group_id": group_id,
                "role": "Applicant",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            try:
                supabase.table("groupmembers").insert(members_data).execute()
            except:
                self._send_error_response("网络错误" ,status_code=404)
                return
            self._send_success_response("申请成功", status_code=200)
                    
            # 用户申请，清除本地用户缓存GROUP_MEMBERS以确保不会重复申请
            global GROUP_MEMBERS
            GROUP_MEMBERS = []
            
        else:
            self._send_error_response("已经位于申请列表内，请等待审核" ,status_code=404)
    else:
        self._send_error_response("已经在该群组内，无需再次申请" ,status_code=404)

        
        
def get_apply(self,post_data_json):
    # 尝试解析json中的userid和token
    try:
        user_id = post_data_json['userid']
    except:
        self._send_error_response("无 user_id包含在json内" ,status_code=400)
        return
    
    # 检查是否为空值
    if user_id is None:
        self._send_error_response("user_id为空", status_code=400)
        return
    

    
    # # 获取全部members信息
    # members_infos = get_group_members(self,user_id,'all')

    # # 获取操作者的群组信息
    # my_members_infos = [message for message in members_infos if message['userid'] == user_id]
    # # 获取操作者担任管理员群组的信息
    # my_admin_in_groups = []
    # for group_info in my_members_infos:
    #     if group_info["role"] in ["Admin", "Owner"]:
    #         my_admin_in_groups.append(group_info)


    # # 获取全部成员的申请列表
    # applicant_members_infos = [message for message in members_infos if message['role'] == 'Applicant']
 
    # applicant_members=[]
    # # 申请类别
    # for infos in applicant_members_infos:
    #     group_id = infos["add_group_id"]
    #     # 操作者担任管理员的群
    #     for my_admin_in_group in my_admin_in_groups:
    #         # 如果申请目标群为操作者管理的群，则添加到applicant_members
    #         if my_admin_in_group["group_id"] == group_id:
    #             applicant_members.append(infos)
    #             break

    # # 获取群组信息
    # group_infos = get_group_list(self)

    # # 遍历每一个数据项在data中
    # for item in applicant_members:
    #     # 提取group_id
    #     group_id = item["group_id"]
    #     # 查找group_infos中的group_id相同的项
    #     for group in group_infos:
    #         if group["group_id"] == group_id:
    #             # 找到匹配项，将group_name存储到data
    #             item["group_name"] = group["group_name"]
    #             break  # 匹配到项后跳出内层循环




    # 重构
    # 优化前的代码中嵌套循环的时间复杂度接近O(n^2)，而优化后的代码时间复杂度主要由列表推导中的单次遍历决定，大致为O(n)。
    # 这意味着随着数据量增加，增长的计算量将是线性的，而不是之前的指数级。

    # 获取全部members信息
    members_infos = get_group_members(self, user_id, 'all')

    # 获取操作者的群组信息
    my_members_infos = [message for message in members_infos if message['userid'] == user_id]

    # 使用集合推导获取操作者担任管理员群组的ID集合
    admin_group_ids = {group_info["group_id"] for group_info in my_members_infos if group_info["role"] in ["Admin", "Owner"]}

    # 获取全部成员的申请列表
    applicant_members_infos = [message for message in members_infos if message['role'] == 'Applicant']

    # 使用列表推导和集合查询快速构造applicant_members列表
    applicant_members = [
        info for info in applicant_members_infos
        if info["add_group_id"] in admin_group_ids
    ]

    # 获取群组信息，并创建一个群组ID到群组名的映射字典
    group_infos = get_group_list(self)
    group_id_to_name = {group["group_id"]: group["group_name"] for group in group_infos}

    # 添加group_name到applicant_members元素
    for item in applicant_members:
        item["group_name"] = group_id_to_name[item["add_group_id"]]
        
    self._send_success_response(applicant_members, status_code=200)
    



def agree(self,post_data_json):
    # 尝试解析json中的userid和token
    try:
        user_id = post_data_json['userid']    # 管理员
        group_id = post_data_json['group_id']  # 申请群
        apply_user_id = post_data_json["apply_user_id"]  # 申请者
    except:
        self._send_error_response("无 user_id,apply_user_id或group_id包含在json内" ,status_code=400)
        return

    # 检查是否为空值
    if group_id is None:
        self._send_error_response("group_id为空", status_code=400)
        return
    if user_id is None:
        self._send_error_response("user_id为空", status_code=400)
        return
    if apply_user_id is None:
        self._send_error_response("apply_user_id为空", status_code=400)
        return
    
    # 处理人是否有权
    admin_user_in_group = get_group_members(self,user_id)
    admin_user_in_group = [message for message in admin_user_in_group if message['group_id'] == group_id]
    role = admin_user_in_group[0]["role"]
    if role != "Admin" and role != "Owner":
        self._send_error_response(f"用户{user_id}权限等级为{role}，权限不足" ,status_code=404)
        return

    # 检测申请状况
    a_user_in_group = get_group_members(self,apply_user_id)
    user_in_add_group = [message for message in a_user_in_group if message['add_group_id'] == group_id]
    if len(user_in_add_group) != 0:
        try:
            supabase.table("groupmembers").update({"add_group_id": None,"group_id": group_id,"role": "Member"}).eq("userid", apply_user_id).execute()
            self._send_success_response(f"已经成功将用户{apply_user_id}添加至{group_id}", status_code=200)
            # 清理缓存
            global GROUP_MEMBERS
            GROUP_MEMBERS = []
        except:
            self._send_error_response("网络错误" ,status_code=404)
            return
    else:
        self._send_error_response(f"没有找到{apply_user_id}在{group_id}该申请", status_code=400)



def create_group(self,post_data_json): 
    try:
        userid = post_data_json['userid']
        group_name = post_data_json['group_name']
    except:
        self._send_error_response("无 userid或group_name包含在json内" ,status_code=400)
        return
    
    group_id = secrets.token_hex(16)

    group_info = get_group_list(self)
    group_info = [message for message in group_info if message['group_id'] == group_id]
    
    if len(group_info) == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "group_id": group_id,
            "group_name": group_name,
            "timestamp": now
        }
        user_data = {
            "userid": userid,
            "group_id": group_id,
            "role": "Owner",
            "timestamp": now
        }
        try:
            supabase.table("groups").insert(data).execute()
            supabase.table("groupmembers").insert(user_data).execute()
        except:
            self._send_error_response("网络错误" ,status_code=404)
            return
        self._send_success_response(f"创建群组成功,群组ID为{group_id},群组名为{group_name}", status_code=200)
        
        # 清除本地群列表缓存
        global GROUPS_INFO
        GROUPS_INFO = []
        # 群聊创建，清除本地用户缓存GROUP_MEMBERS以确保创建者申请入群
        global GROUP_MEMBERS
        GROUP_MEMBERS = []

    else:
        self._send_error_response("出现了及其稀有的错误呢" ,status_code=400)


    

    

def get_group(self,post_data_json): 
    try:
        userid = post_data_json['userid']
    except:
        self._send_error_response("无 userid或group_name包含在json内" ,status_code=400)
        return
    
    # 获取用户在群组的信息
    members_infos = get_group_members(self,userid)
    members_infos = [message for message in members_infos if message['userid'] == userid]
    data = []
    for group_info in members_infos:
        if group_info["role"] in ["Member", "Admin", "Owner"]:
            data.append(group_info)
    
    # 获取群组信息
    group_infos = get_group_list(self)


    # 遍历每一个数据项在data中
    for item in data:
        # 提取group_id
        group_id = item["group_id"]
        # 查找group_infos中的group_id相同的项
        for group in group_infos:
            if group["group_id"] == group_id:
                # 找到匹配项，将group_name存储到data
                item["group_name"] = group["group_name"]
                break  # 匹配到项后跳出内层循环


    self._send_success_response(data, status_code=200)



def search_group(self,post_data_json):
    def search_groups(groups, term):
        # 将搜索词转换为小写并编译成正则表达式以进行模糊匹配
        pattern = re.compile(re.escape(term.lower()))
        # 准备存储结果的列表
        search_results = []
        # 遍历所有群聊数据
        for group in groups:
            # 对群聊名称、ID和时间进行小写转换，并检查是否有匹配
            if any(pattern.search(item.lower()) if item is not None else '' for item in (group['group_name'], group['group_id'], group['timestamp'])):
                search_results.append(group)
        return search_results
    
    try:   
        # 要搜索的词
        group_search_term = post_data_json['group_search_term']
    except:
        self._send_error_response("无 group_search_term包含在json内" ,status_code=400)
        return

    try:   
        # 群聊信息列表
        example_groups = get_group_list(self)

        # 调用搜索函数并打印结果
        search_results = search_groups(example_groups, group_search_term)
        self._send_success_response(search_results, status_code=200)
    except:
        return


    