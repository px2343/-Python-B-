'''
  B站弹幕爬虫
  程序功能：从B站爬取王心凌相关视频弹幕，并将数据保存到CSV文件中
'''

import re  # 正则表达式提取文本
import requests  # 爬虫发送请求（向网站发送请求）
from bs4 import BeautifulSoup as BS  # 爬虫解析页面（解析HTML/XML页面）
import time
import pandas as pd  # 存入csv文件（处理数据并存储为CSV文件）
import os


def get_bilibili_danmu(v_url, v_result_file):
	"""
	获取B站弹幕并保存到文件中
	:param v_url: 视频地址
	:param v_result_file: 保存文件名
	:return:
	"""
	# 定义字典 headers，用于设置请求头信息，在请求B站的网页时会用到
	headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)", }  # 客户端使用的是 Mozilla Firefox 浏览器
	print('视频地址是：', v_url)
	# 使用 requests 模块向 Bilibili 的API地址发送GET请求，请求参数为 bv，响应结果按JSON格式返回。响应结果以 r1 对象保存
	r1 = requests.get(url='https://api.bilibili.com/x/player/pagelist?bvid='+bv, headers=headers)  # 使用requests模块发送请求获取数据(r1对象包括了相应网页的状态码、响应头和响应体等信息)
	# 解析后的结果可以使用字典语法访问和处理
	html1 = r1.json()  # 调用 json() 方法，将响应体解析为一个 Python 字典，保存在 html1 变量中
	cid = html1['data'][0]['cid']  # 获取视频对应的cid(Comment ID)号(获取含有视频信息的字典 html1，然后通过字典索引方式（即使用键索引值）获取到该视频对应的 cid)
	print('该视频的cid是:', cid)
	danmu_url = 'http://comment.bilibili.com/{}.xml'.format(cid)  # 弹幕地址
	print('弹幕地址是：', danmu_url)
	r2 = requests.get(danmu_url)
	html2 = r2.text.encode('raw_unicode_escape')  # 编码格式
	soup = BS(html2, 'xml')
	danmu_list = soup.find_all('d')
	print('共爬取到{}条弹幕'.format(len(danmu_list)))
	video_url_list = []  # 视频地址
	danmu_url_list = []  # 弹幕地址
	time_list = []  # 弹幕时间
	text_list = []  # 弹幕内容
	for d in danmu_list:
		data_split = d['p'].split(',')  # 按逗号分隔
		temp_time = time.localtime(int(data_split[4]))  # 转换时间格式
		danmu_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time)
		video_url_list.append(v_url)
		danmu_url_list.append(danmu_url)
		time_list.append(danmu_time)
		text_list.append(d.text)
		print('{}:{}'.format(danmu_time, d.text))
	df = pd.DataFrame()  # 初始化一个DataFrame对象
	df['视频地址'] = video_url_list
	df['弹幕地址'] = danmu_url_list
	df['弹幕时间'] = time_list
	df['弹幕内容'] = text_list
	if os.path.exists(v_result_file):  # 如果文件存在，不需写入字段标题
		header = None
	else:  # 如果文件不存在，说明是第一次新建文件，需写入字段标题
		header = ['视频地址', '弹幕地址', '弹幕时间', '弹幕内容']
	df.to_csv(v_result_file, encoding='utf_8_sig', mode='a+', index=False, header=header)  # 数据保存到csv文件


if __name__ == "__main__":  # 程序的入口
	print('爬虫程序开始执行！')
	# 保存数据的文件名
	csv_file = '王心凌弹幕.csv'
	# 如果存在csv文件，先删除，避免数据重复
	if os.path.exists(csv_file):
		print('{}已存在，开始删除文件'.format(csv_file))
		os.remove(csv_file)
		print('{}已删除文件'.format(csv_file))
	# "王心凌"弹幕数较多的视频Bv号
	bv_list = ['BV1qY4y157dz', 'BV1a34y1E73C',]  # 视频列表
	# 开始爬取（对视频列表进行遍历，并将获取到的数据保存到CSV文件中）
	for bv in bv_list:
		get_bilibili_danmu(v_url='https://www.bilibili.com/video/{}'.format(bv), v_result_file='王心凌弹幕.csv')
	print('爬虫程序执行完毕！')
