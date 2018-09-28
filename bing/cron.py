import requests
from bs4 import BeautifulSoup
from bing.models import Mpic
from PIL import Image

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
} 

def my_scheduled_job():
	url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
	respon = requests.get(url)
	title = respon.json()['images'][0]['copyright']
	date = respon.json()['images'][0]['enddate']
	pub_date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
	if Mpic.objects.filter(pub_date=pub_date):
		print('已存在')
	else:
		# 获取图片路径
		pic_small='bing/' + pub_date + '.jpg'
		imgurl = 'cn.bing.com' + respon.json()['images'][0]['url']
		# 获取介绍
		descripreq = requests.get('https://cn.bing.com/cnhp/life')
		descripsoup = BeautifulSoup(descripreq.text,'html.parser')
		descrip = descripsoup.select('#hplaSnippet')[0].string
		# 写入数据
		Mpic.objects.create(title=title,description=descrip,pub_date=pub_date,pic_small=pic_small,pic_full=imgurl)
		# 用pillow生成缩小图，图片存放路径，django下有效
		fullpic = 'media/bing_full/'  + pub_date + '.jpg'
		img_path = 'media/bing/' + pub_date + '.jpg'
		img = requests.get('https://'+imgurl)
		with open(fullpic, 'wb') as file:
		    file.write(img.content)
		file.close()
		im = Image.open(fullpic)
		w, h = im.size
		im.thumbnail((w*0.3, h*0.3))	# 缩放到30%:
		im.save(img_path, 'jpeg')

def bingspide():
	# for p in range(11,12):
	# 	respon = requests.get('https://bing.ioliu.cn/?p=' + str(p), headers = headers)
		respon = requests.get('https://bing.ioliu.cn/', headers = headers)
		soup = BeautifulSoup(respon.text,'html.parser')
		date = soup.select('.calendar em')
		imgurl = soup.find_all(class_='mark')
		picurl = []
		for i in range(0,len(imgurl)):
			pub_date = date[i].string
			picurl.append('https://bing.ioliu.cn' + imgurl[i]['href'])
			picsoup = BeautifulSoup(requests.get(picurl[i], headers = headers).text,'html.parser')
			descrip=picsoup.select('.sub')[0].string
			title = picsoup.select('.title')[0].string
			pic_small = 'bing/' + pub_date + '.jpg'
			img_url = imgurl[i]['href']
			pic_full_url = 'h1.ioliu.cn/bing'+img_url[6:img_url.rindex('?force')] + '_1920x1080.jpg'
			Mpic.objects.get_or_create(title=title,description=descrip,pub_date=pub_date,pic_small=pic_small,pic_full=pic_full_url)

			# 用pillow生成缩小图，图片存放路径，concent with cmd path
			fullpic = 'media/bing_full/' + pub_date + '.jpg'
			img_path = 'media/bing/' + pub_date + '.jpg'
			print(pic_full_url)
			img = requests.get('http://'+pic_full_url, headers = headers)

			with open(fullpic, 'wb') as file:
			    file.write(img.content)
			file.close()
			
			im = Image.open(fullpic)
			w, h = im.size
			im.thumbnail((w*0.3, h*0.3))	# 缩放到30%:
			im.save(img_path, 'jpeg')

			print(pub_date+'saved success')

# my_scheduled_job()
# bingspide()

# headers = {
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# } 
# img = requests.get('http://h1.ioliu.cn//bing/TrinityLibrary_EN-AU10332583093_1920x1080.jpg', headers = headers)
# print(img)