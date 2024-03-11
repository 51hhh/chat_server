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

2024.3.8更新：修复部分问题，更改储存用户信息为数据库，添加部分注释，更改响应结构，完善部分功能。 2024.3.8

![image](https://github.com/51hhh/chat_server/assets/87711493/43d4a999-8979-477a-9fde-3af180ee7020)

--------------------------------------------------------

2024.3.9更新，开始web设计和编写，发现原本后端部分较为严重问题。

目前计划
+ 规范后端api文档
+ 后端功能维护
+ 前端页面设计


--------------------------------------------------------

2024.3.10更新，修改参数传递发送为json而不是Query 参数明文发送，修复发送消息没有鉴权的bug，修复缺少参数引起异常的错误，打包部分重复代码进行复用，添加部分注释。修复后端/chat_web传递null的问题。

实现基本的注册登录，读取信息的基本功能，具体还需进一步测试。第一次用css，太难调了/(ㄒoㄒ)/~~

--------------------------------------------------------

2024.3.11
更新

后端：对getmessag的用户鉴权和message增加本地缓存机制，避免前端轮询时对数据库造成重复请求，同时提示请求速度。

前端：message页面实现轮询更新消息，自动滑动至底部，dom平滑滚动更新。
