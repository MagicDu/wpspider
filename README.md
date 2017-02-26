## 利用python-wordpress-xmlrpc库整合Python爬虫，实现自动化发布文章到自己的wordpress

### 环境说明
* WordPress 3.4+ OR WordPress 3.0-3.3 with the XML-RPC Modernization Plugin.
* Python 3.x  
* Ubunutu 16.04
* install python-wordpress-xmlrpc
```bash
    sudo pip3 install python-wordpress-xmlrpc
```
* 只是以某单一的网站为例，抓取其他网站，请自行重写``get_news(url)``函数
* 功能尚未完善，今后会继续添加
### 2017-02-26 v1.0.0

1.实现了抓取单个文章的内容发布到wordpress

2.提取了文章标题，标签，内容，分类

