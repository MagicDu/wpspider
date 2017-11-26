#!/usr/bin/env python3
#-*-coding : utf-8 -*-
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.methods.posts import GetPosts,NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from email.mime.text import MIMEText
from email.header import Header
import re
import time
import smtplib
import traceback
import os,random
import requests

user_agents=list()
#新闻类
class News(object):
	def __init__(self,title,tags,category,content,image_name):
		self.title = title     #标题
		self.tags=tags         #标签
		self.category=category #分类
		self.content=content   #内容
		self.image_name=image_name

# 根据url 获取主机名
def getHost(url):
    reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
    m = re.match(reg, url)
    uri = m.groups()[0] if m else ''
    host=uri[uri.rfind('.', 0, uri.rfind('.')) + 1:]
    return host

#获取最新的新闻链接列表

'''
url  :需要抓取的网址
n    :获取链接的数量,即每次需要发布新文章的数量
links:返回链接列表
'''
def get_urls(url,n=1):
	links=[]
	length = len(user_agents)
	index=random.randint(0,length-1)
	user_agent = user_agents[index]
	headers={
		'Referer': 'http://www.jrzj.com',
		'Host':'www.jrzj.com',
		'User-Agent':user_agent,
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	bsObj=requests.session()
	bsObj=BeautifulSoup(bsObj.get(url,headers=headers).content,'html.parser')
	for link in bsObj.find('div',{'class':'main2_left_fir_left'}).findAll('a')[0:n]:
		if 'href' in link.attrs:
			links.append(link.attrs['href'])
	return links

#加载 user_agents配置文件
def load_user_agent():
	fp = open('user_agents', 'r')
	line  = fp.readline().strip('\n')
	while(line):
		user_agents.append(line)
		line = fp.readline().strip('\n')
	fp.close()

#根据文章链接切分文章
'''
这里是以金融之家为例的,抓取其他资讯请自行分析网站文章重写 get_news(link)
'''
def get_news(link):
	length = len(user_agents)
	index=random.randint(0,length-1)
	user_agent = user_agents[index]
	headers={
		'Referer': 'http://www.jrzj.com',
		'Host':'www.jrzj.com',
		'User-Agent':user_agent,
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	bsObj=requests.session()
	bsObj=BeautifulSoup(bsObj.get(link,headers=headers).content,'html.parser')
	title=bsObj.h1.get_text()
	#print('标题:',title)
	tags_list=bsObj.find('meta',{'name':'keywords'}).attrs['content']
	l=re.split(',',tags_list)
	tags=[item for item in filter(lambda x:x != '', l)]
	#print('标签:',tags)
	category=bsObj.title.get_text().split('_')[1]
	#print('分类',category)
	#content=bsObj.find('div',{'class':'news_content'}).prettify()
	content=bsObj.find('div',{'class':'news_content'})
	#print('内容:',content)
	#查找图片
	a_tag=content.find('img')
	#print(a_tag)
	image_url=a_tag.attrs['src']
	image_name=os.path.basename(image_url).split('!')[0]
	#下载图片
	get_image(image_url,image_name)
	#删除标签
	a_tag.extract()
	news=News(title,tags,category,content.prettify(),image_name)
	return news

#下载图片
'''
将图片保存到本地
'''
def get_image(image_url,image_name):
	os.makedirs('images',exist_ok=True)
	#print('下载了--->'+image_name)
	urlretrieve(image_url,'images/'+image_name)


#上传图片
'''
根据图片路径将图片上传到wordpress

返回attachment_id
'''
def upload_image(image_name,client):
	data={
		'name':image_name,
		'type':'image/jpeg'
	}
	with open('images/'+image_name, 'rb') as img:
		data['bits'] = xmlrpc_client.Binary(img.read())
	response = client.call(media.UploadFile(data))
	#print('上传了--->'+image_name)
	attachment_id = response['id']
	return attachment_id

#发送新闻到wordpress

'''
yourwebsit: 你的wordpress地址+xmlrpc.php
username  : wordpress登录用户名
password  : wordpress登录密码
news      : 新闻对象
'''

def send_news(yourwebsit,username,password,news):
	wp=Client(yourwebsit,username,password)
	attachment_id=upload_image(news.image_name,wp)
	post=WordPressPost()
	post.title=news.title
	post.content=news.content
	post.post_status ='publish'
	post.thumbnail = attachment_id
	post.terms_names={
		'post_tag':news.tags,
		'category':[news.category]
	}
	wp.call(NewPost(post))



#将文章标题写入文件
def write_file(str_title):
	with open('title.txt','a') as f:
		f.write(str_title)

#发送电子邮件
'''
mail_user   :发送者名称
mail_postfix:邮箱后缀
sender      :发送者
receiver    :接收者(可以设置为139邮箱)
smtpserver  :smtp服务器地址
message     :消息
subject     :主题
username    :用户名
password    :密码
example: 以新浪邮箱为例
send_email('user','sina.com','user@sina.com','xxxx@qq.com','smtp.sina.com','您的爬虫出现异常\n'+m,'wpspider','user@sina.com','abc123')
'''

def send_email(mail_user,mail_postfix,sender,receiver,smtpserver,message,subject,username,password):
	try:
		msg=MIMEText(message,'plain','utf-8')
		me="Wpspider"+"<"+mail_user+"@"+mail_postfix+">" 
		msg['From']=Header(me)
		msg['Subject']=Header(subject,'utf-8')
		smtp = smtplib.SMTP()
		smtp.connect(smtpserver)
		smtp.login(username,password)
		smtp.sendmail(sender, receiver, msg.as_string())
		smtp.quit()
		print ("邮件发送成功")
	except smtplib.SMTPException as e:
		print ("Error: 无法发送邮件")
	

#以金融之家为例
#接收邮箱可以设置为139邮箱，以便接收短信提醒
try:
	load_user_agent()
	l=get_urls('http://www.jrzj.com',1)
	for link in l:
		news=get_news(link)
		#print(news.title) #打印文章标题
		write_file(news.title+'\n')
		time.sleep(5)
		send_news('http://blog.abc.com/xmlrpc.php','username','password',news)
except Exception as e:
	m=traceback.format_exc()
	send_email('user','sina.com','user@sina.com','xxxx@139.com','smtp.sina.com','您的爬虫出现异常\n'+m,'wpspider','user@sina.com','abc123')