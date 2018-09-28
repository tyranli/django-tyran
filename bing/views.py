from django.shortcuts import render,get_object_or_404
from .models import Mpic
from django.core.paginator import Paginator
from count.views import count_once_read
# Create your views here.

def pic_list(request):
	paged_list = Paginator(Mpic.objects.all(), 12)	#取所有的blog进行每10篇分页，分页后的blog
	page_num = request.GET.get('page', 1)	#取页面传过来的参数，对应?page=x，GET方法。默认值为1。
	paged_pics = paged_list.get_page(page_num)	#取特定页的博客

	context = {}
	context['Tpics'] = paged_pics
	return render(request,'index.html',context)

def pic_detail(request,pic_date):
	onepic = get_object_or_404(Mpic,pub_date=pic_date)
	read_cookie_key = count_once_read(request, onepic)

	context = {}
	context['onepic'] = onepic
	context['previous_pic'] = Mpic.objects.filter(pub_date__gt=onepic.pub_date).last() #上一篇
	context['next_pic'] = Mpic.objects.filter(pub_date__lt=onepic.pub_date).first() #下一篇
	response = render(request,'pic_detail.html',context)
	response.set_cookie(read_cookie_key, 'true')
	return response