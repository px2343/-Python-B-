# 弹幕的情感分析

import pandas as pd  # 数据分析库
from snownlp import SnowNLP  # 中文情感分析库
from wordcloud import WordCloud  # 绘制词云图
from pprint import pprint  # 美观打印
import jieba.analyse  # jieba分词
from PIL import Image  # 读取图片
import numpy as np  # 将图片的像素点转换成矩阵数据
import matplotlib.pyplot as plt  # 画图

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 情感分析打分
def sentiment_analyse(v_cmt_list):
	"""
	情感分析打分
	:param v_cmt_list: 需要处理的评论列表
	:return:
	"""
	score_list = []  # 情感评分值
	tag_list = []  # 打分分类结果
	pos_count = 0  # 计数器-积极
	neg_count = 0  # 计数器-消极
	mid_count = 0  # 计数器-中性
	for comment in v_cmt_list:
		tag = ''
		sentiments_score = SnowNLP(comment).sentiments
		if sentiments_score < 0.5:
			tag = '消极'
			neg_count += 1
		elif sentiments_score > 0.5:
			tag = '积极'
			pos_count += 1
		else:
			tag = '中性'
			mid_count += 1
		score_list.append(sentiments_score)  # 得分值
		tag_list.append(tag)  # 判定结果
	df['情感得分'] = score_list
	df['分析结果'] = tag_list
	grp = df['分析结果'].value_counts()
	print('正负面评论统计：')
	print(grp)
	grp.plot.pie(y='分析结果', autopct='%.2f%%')  # 画饼图
	plt.title('王心凌弹幕_情感分布占比图')
	plt.savefig('王心凌弹幕_情感分布占比图.png')  # 保存图片
	plt.show()
	# 把情感分析结果保存到excel文件
	df.to_excel('王心凌弹幕_情感评分结果.xlsx', index=None)
	print('情感分析结果已生成：王心凌_情感评分结果.xlsx')


def make_wordcloud(v_str, v_stopwords, v_outfile):
	"""
	绘制词云图
	:param v_str: 输入字符串
	:param v_stopwords: 停用词
	:param v_outfile: 输出文件
	:return: None
	"""
	print('开始生成词云图：{}'.format(v_outfile))
	try:
		stopwords = v_stopwords  # 停用词
		backgroud_Image = np.array(Image.open('王心凌_背景图.png'))  # 读取背景图片
		wc = WordCloud(
			background_color="white",  # 背景颜色
			width=1500,  # 图宽
			height=1200,  # 图高
			max_words=1500,  # 最多字数
			font_path="C:\Windows\Fonts\simhei.ttf",  # 字体文件路径，(Windows)
			stopwords=stopwords,  # 停用词
			mask=backgroud_Image,  # 背景图片
		)
		jieba_text = " ".join(jieba.lcut(v_str))  # jieba分词
		wc.generate_from_text(jieba_text)  # 生成词云图
		wc.to_file('王心凌弹幕_词云图.png')  # 保存图片文件
		plt.imshow(wc, interpolation='bilinear')
		plt.axis("off")
		plt.show()
		print('词云图生成成功：王心凌弹幕_词云图.png')

	except Exception as e:
		print('make_wordcloud except: {}'.format(str(e)))



if __name__ == '__main__':
	df = pd.read_csv('王心凌弹幕.csv')  # 读取excel
	v_cmt_list = df['弹幕内容'].values.tolist()  # 评论内容列表
	print('length of v_cmt_list is:{}'.format(len(v_cmt_list)))
	v_cmt_list = [str(i) for i in v_cmt_list]  # 数据清洗-list所有元素转换成字符串
	v_cmt_str = ' '.join(str(i) for i in v_cmt_list)  # 评论内容转换为字符串
	# 1、情感分析打分
	sentiment_analyse(v_cmt_list=v_cmt_list)
	# 2、用jieba统计弹幕中的top10高频词
	keywords_top10 = jieba.analyse.extract_tags(v_cmt_str, withWeight=True, topK=10)
	print('top10关键词及权重：')
	pprint(keywords_top10)
	with open('TOP10高频词.txt', 'w') as f:
		for i in keywords_top10:
			f.write(str(i[0]) + ' ' + str(i[1]))  # i[0]是关键词，i[1]是权重值
			f.write('\n')  # 换行

	# 3、画词云图
	make_wordcloud(v_str=v_cmt_str,
	               # 停用词
	               v_stopwords=['这个', '吗', '的', '啊', '她', '是', '了', '你', '我', '都', '也', '不', '在', '吧', '说', '就是', '这',
	                            '有', '就', '或', '哇', '哦', '这样', '真的', '还'],
	               # 词云图文件名
	               v_outfile='王心凌弹幕_词云图.jpg'
	               )

