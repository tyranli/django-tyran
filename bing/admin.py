from django.contrib import admin

from .models import Mpic
# Register your models here.

@admin.register(Mpic)
class MpicAdmin(admin.ModelAdmin):
	list_display = ('title','pub_date','get_read_num')
	search_fields = ('title',) 				#增加搜索框，根据title来搜索，要求是列表，必须加“,”
	# list_filter = ('location',) 				#设置一个过滤器，根据'title'内容分类来过滤，