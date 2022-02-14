"""mathanalysing URL Configuration--copied

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url,include
from . import views

app_name = 'dxfc'
urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$',views.homepage),
    url(r'^dimension/add',views.add_dimension),
    url(r'^dimension/list',views.list_dimension),
    url(r'^dimension/edit/(\d+)',views.modify_dimension),
    url(r'^dimension/del/(\d+)',views.del_dimension)
    # path(r'page1',views.page1),
    # # re_path 等同 url,需要^指定开头筛选,（）分组中是字符串
    # url(r'^number/(\d{1,10})',views.number),
    # url(r'^person/(?P<name>\w+)/(?P<age>\d+)',views.person),
    # url(r'^birthday/(\d{4})/(\d{1,2})/(\d{1,2})',views.birthday),
    # url(r'^(\d{1,10})/add/(\d{1,10})',views.add),
    # url(r'test_get',views.test_get),
    # url(r'birthday',views.birthday),
    # url(r'^search$',views.search),
    # url(r'^shebao$',views.shebao),
    # url(r'^show_image',views.show_image),
    # url(r'^math/',include('mathanalysing.urls')),
    # # path默认year必须全匹配了，传递的year是int类型
    # path(r'year/<int:year>',views.year)
]