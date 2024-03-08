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

--------------------------------------------------------

更新：修复部分问题，更改储存用户信息为数据库，添加部分注释，更改响应结构，完善部分功能。 2024.3.8：21：33

![image](https://github.com/51hhh/chat_server/assets/87711493/43d4a999-8979-477a-9fde-3af180ee7020)
