from django.db import models
from count.models import ReadNumExpandMethod
# Create your models here.

class Mpic(models.Model,ReadNumExpandMethod):
	title = models.CharField('标题',max_length = 100)
	description = models.TextField('介绍')
	pub_date = models.DateField('发布时间')
	pic_small = models.FileField('缩略图路径', upload_to='bing')
	pic_full = models.FileField('大图路径', upload_to='bing')

	class Meta:
		verbose_name_plural = verbose_name = 'Bing每日美图'
		ordering = ['-pub_date']
		
	def __str__(self):
		return self.title