#!/usr/bin/env python3
#-*-coding : utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts,NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import re


#新闻类
class News(object):
	def __init__(self,title,tags,category,content):
		self.title = title     #标题
		self.tags=tags         #标签
		self.category=category #分类
		self.content=content   #内容


#根据文章链接切分文章
'''
这里是以金融之家为例的,抓取其他资讯请自行分析网站文章重写 get_news(url)
'''
def get_news(url):
	html=urlopen(url)
	bsObj=BeautifulSoup(html,'html.parser')
	title=bsObj.h1.get_text()
	#print('标题:',title)
	tags=bsObj.find('meta',{'name':'keywords'}).attrs['content']
	#print('标签:',tags)
	category=bsObj.title.get_text().split('_')[1]
	#print('分类',category)
	content=bsObj.find('div',{'class':'news_content'}).prettify()
	#print('内容:',content)
	news=News(title,tags,category,content)
    return news

#发送新闻到wordpress

'''
yourwebsit: 你的wordpress地址+xmlrpc.php
username:wordpress登录用户名
password:wordpress登录密码
news:新闻对象
'''

def send_news(yourwebsit,username,password,news):
	wp=Client(yourwebsit,username,password)
	post=WordPressPost()
	post.title=news.title
	post.content=news.content
	post.post_status ='publish'
	post.terms_names={
		'post_tag':re.split(',',news.tags),
		'category':[news.category]
	}
	wp.call(NewPost(post))


#函数调用示例：
news=get_news('http://www.jrzj.com/180636.html')
send_news('http://www.baidu.com/xmlrpc.php','abc','123',news)

