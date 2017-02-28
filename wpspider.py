#!/usr/bin/env python3
#-*-coding : utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts,NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import re
import time


#新闻类
class News(object):
	def __init__(self,title,tags,category,content):
		self.title = title     #标题
		self.tags=tags         #标签
		self.category=category #分类
		self.content=content   #内容

#获取最新的新闻链接列表

'''
url  :需要抓取的网址
n    :获取链接的数量,即每次需要发布新文章的数量
links:返回链接列表
'''
def get_urls(url,n=1):
	links=[]
	html=urlopen(url)
	bsObj=BeautifulSoup(html,'html.parser')
	for link in bsObj.find('div',{'class':'main2_left_fir_left'}).findAll('a')[0:n]:
		if 'href' in link.attrs:
			links.append(link.attrs['href'])
	return links


#根据文章链接切分文章
'''
这里是以金融之家为例的,抓取其他资讯请自行分析网站文章重写 get_news(link)
'''
def get_news(link):
	html=urlopen(link)
	bsObj=BeautifulSoup(html,'html.parser')
	title=bsObj.h1.get_text()
	#print('标题:',title)
	tags_list=bsObj.find('meta',{'name':'keywords'}).attrs['content']
	l=re.split(',',tags_list)
	tags=[item for item in filter(lambda x:x != '', l)]
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
username  : wordpress登录用户名
password  : wordpress登录密码
news      : 新闻对象
'''

def send_news(yourwebsit,username,password,news):
	wp=Client(yourwebsit,username,password)
	post=WordPressPost()
	post.title=news.title
	post.content=news.content
	post.post_status ='publish'
	post.terms_names={
		'post_tag':news.tags,
		'category':[news.category]
	}
	wp.call(NewPost(post))



#将文章标题写入文件
def write_file(str_title):
	with open('/mysoft/py/title.txt','a') as f:
		f.write(str_title)

#以金融之家为例
l=get_urls('http://www.jrzj.com',3)
for link in l:
	news=get_news(link)
	#print(news.title) #打印文章标题
	write_file(news.title)
	time.sleep(5)
	send_news('http://blog.abc.com/xmlrpc.php','username','password',news)

