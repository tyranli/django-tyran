"""tyran URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from bing.views import pic_list, pic_detail

# 定时任务
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
from bing import cron

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pic_list),
    path('bing/<str:pic_date>',pic_detail,name='pic_detail'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


 # 定时任务
sched = BackgroundScheduler()
# @sched.scheduled_job('interval',days = 1,hours = 0,minutes = 0,seconds = 0)
@sched.scheduled_job('date', run_date=datetime(2018, 9, 9, 0, 55, 50))
def my_task():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # cron.my_scheduled_job()
    cron.bingspide()
sched.start()

#表示每隔3天17时19分07秒执行一次任务
# 'interval',days = 03,hours = 17,minutes = 19,seconds = 07
#定时执行2009年11月6日的16:30:05
# 'date', run_date=datetime(2009, 11, 6, 16, 30, 5)