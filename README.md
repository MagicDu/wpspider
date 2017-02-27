## 利用python-wordpress-xmlrpc库整合Python爬虫，实现自动化发布文章到自己的wordpress

### 环境说明
* WordPress 3.4+ OR WordPress 3.0-3.3 with the XML-RPC Modernization Plugin.
* Python 3.x  
* Ubunutu 16.04
* install python-wordpress-xmlrpc
```bash
    sudo pip3 install python-wordpress-xmlrpc
```
* 只是以某单一的网站为例，抓取其他网站，请自行重写``get_news(link)``,``get_urls(url,n)``函数
* 功能尚未完善，今后会继续添加

### 版本说明

#### 2017-02-26  v1.0.0

    1.实现了抓取单个文章的内容发布到wordpress

    2.提取了文章标题，标签，内容，分类

#### 2017-02-27  v1.0.1
    1.增加‘获取最新的新闻链接列表’的函数``get_urls(url,n)``
    
    2.遍历获取的新链接列表发布文章到wordpress，文章数量可以通过参数``n``指定，默认值为``1``
    
    3.增加发布下一篇文章之前，休眠5秒
