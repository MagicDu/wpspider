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
* 保存文章标题到本地，需要在``write_file(str_title)``指定你的文件路径
* crontab自动执行脚本，需要Python3.5 安装python-crontab,**仅适用于linux,windows和Mac请自行写自动执行脚本** 运行脚本前，请指定将要运行的爬虫目录，以及运行时间，具体参考crontab的说明
* sh脚本适用于crontab无法直接执行python脚本的问题，需要用crontab执行sh脚本，sh脚本调用python脚本
```bash
    sudo pip3 install python-crontab
```
* 功能尚未完善，今后会继续添加

### 版本说明

#### 2017-02-26  v1.0.0

    1.实现了抓取单个文章的内容发布到wordpress

    2.提取了文章标题，标签，内容，分类

#### 2017-02-27  v1.0.1
    1.增加‘获取最新的新闻链接列表’的函数 get_urls(url,n)
    
    2.遍历获取的新链接列表发布文章到wordpress，文章数量可以通过参数n指定，默认值为1
    
    3.增加发布下一篇文章之前，休眠5秒
#### 2017-02-28  v1.0.2
    1.修复标签为空时无法发布文章的bug

    2.增加将文章标题保存到本地文件的功能 write_file(str_title)

    3.增加了crontab 自动执行脚本 “createCronTab.py”
#### 2017-03-01
    1.增加wp.sh脚本，如果服务器上的crontab直接执行python脚本出错，需要用crontab调用sh脚本，sh脚本调用python脚本（主要是crontab执行环境变量与系统环境变量存在差异）

### Bug说明

#### 单一性

    1.目前处理的只是一个网站 金融之家的内容作为示例

    2.获取的文章内容还未经过提取处理，只是字符串发布
#### 异常处理

**该程序尚未对异常做出处理**


### TodoList

#### 异常处理
    1.处理异常，记录日志

    2.处理异常，发送邮件

#### 爬虫适应性提升
    1.多网站

**未完待续。。。**



