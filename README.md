计划开发一个在线聊天后端，进行简单的逻辑判断，用户鉴权，消息储存。

第一次进行开发，希望规范相关格式，如API接口，注释，代码，即文档。

## 使用方法
可以使用vercel部署

<p dir="auto"><a href="https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F51hhh%2Fchat_server" rel="nofollow"><img src="" alt="Deploy with Vercel" data-canonical-src="https://vercel.com/button" style="max-width: 100%;"></a></p>

## 创建数据库
https://supabase.com/

github或者google登录，创建一个数据库，找到连接即可。

![image](https://github.com/51hhh/chat_server/assets/87711493/37aa4ade-d6e2-4d85-82c7-1ba70baf217a)

![image](https://github.com/51hhh/chat_server/assets/87711493/09a04a7a-50cb-4ab4-b72a-fdd7e73a7f2e)

![image](https://github.com/51hhh/chat_server/assets/87711493/84df2d53-dfbf-4143-8dfe-207d84e9b2c1)

分别为url和key。

## 添加环境变量

![image](https://github.com/51hhh/chat_server/assets/87711493/7f938b14-e6b5-4760-b7a8-a076569c45e1)

![image](https://github.com/51hhh/chat_server/assets/87711493/fb4ca80d-77d3-4129-9d1a-2c6601f558f3)

在这里分别填写`SUPABASE_URL`和`SUPABASE_KEY`即上面获取的url和key。

![image](https://github.com/51hhh/chat_server/assets/87711493/8b80b18b-04e8-48bb-8152-ce97da2e5cdd)

## api请求

部署后为根目录的/api下，即若你在vercel自定义域名为https://chatserve.polar-bear.eu.org，则api为https://chatserve.polar-bear.eu.org/api/

api文档

https://apifox.com/apidoc/shared-135607bc-4296-40dd-9835-4129ab657c38

--------------------------------------------------------

2024.3.8-2024.3.18

更新：修复部分问题，更改储存用户信息为数据库，添加部分注释，更改响应结构，完善部分功能。

![image](https://github.com/51hhh/chat_server/assets/87711493/43d4a999-8979-477a-9fde-3af180ee7020)

开始web设计和编写，修复后端部分问题。

目前计划
+ 规范后端api文档
+ 后端功能维护
+ 前端页面设计

修改参数传递发送为json而不是Query 参数明文发送，修复发送消息没有鉴权的bug，修复缺少参数引起异常的错误，打包部分重复代码进行复用，添加部分注释。修复后端/chat_web传递null的问题。

实现基本的注册登录，读取信息的基本功能，具体还需进一步测试。第一次用css，太难调了/(ㄒoㄒ)/~~

对getmessag的用户鉴权和message增加本地缓存机制，避免前端轮询时对数据库造成重复请求，同时提示请求速度。

message页面实现轮询更新消息，自动滑动至底部，dom平滑滚动更新。

css布局更新聊天页面容器布局调整，自己消息靠右区分，发送款即按钮样式修改，添加发送消息功能，修复部分错误，优化代码注释。

![](https://cdn.ziyourufeng.eu.org/51hhh/img_bed/main/img/2024.3.10/20240312212812.png)

窗口大小实现初步自适应调整。

将“关系型数据库”设计的范式来设计群聊数据库结构提上日程。

对多群组聊天架构开始设计

一个是群组表（Groups），用以存储群组的基本信息；另一个是群成员表（GroupMembers），用于存储群组成员的信息。如果你需要存储消息，还可以设计一个消息表（Messages）来存储群聊消息。

以下是一个基础的表格设计示例：

群组表（Groups）：
- GroupID：唯一标识每个群组的ID。
- GroupName：群组的名称。
- CreateTime：群组创建的时间。
- OtherInfo：如群组描述、群组头像等其他信息。

群成员表（GroupMembers）：
- MemberID：唯一标识每个成员的ID。
- GroupID：成员所在群组的ID。
- JoinTime：成员加入群组的时间。
- MemberRole：成员在群组中的角色（例如：管理员、普通成员）。

消息表（Messages）：
- MessageID：唯一标识每条消息的ID。
- GroupID：消息所属的群组ID。
- SenderID：发送消息成员的ID。
- MessageContent：消息内容。
- SendTime：消息发送的时间。

在这种设计方案中，GroupID 是关联“群组表”和“群成员表”的外键。这样你可以通过一个群组ID就能查询到该群组所有的成员，同时群组和消息也是通过 GroupID 关联的。


![image](https://github.com/51hhh/chat_server/assets/87711493/ffd43c4b-e229-434c-9386-810830bb0978)

-----------------------------------------------------------------------
2024.3.19-2024.4.9

优化后端缓存机制，新增apply_for，agree，get_apply，create_group，get_group，search_group接口，实现关系型数据库架构，完善鉴权机制，防止恶意越权调用，完善权限等级隔离，防止非法获取无权限信息，优化程序结构，增加部分错误处理，提示容错率，修复多个恶性bug。

对css页面设计进行美化，更改部分配色，页面实现自适应（移动端未实现），丰富页面效果，添加部分动画，提高交互能力，对侧边栏重构，新增群组切换功能，添加加群和审核功能。

+ 实现多群聊功能
+ 实现加群功能
+ 实现审核功能
