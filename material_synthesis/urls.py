"""定义learning_logs的URL模式"""
from django.urls import path

from . import views

app_name = 'material_synthesis'
urlpatterns = [
	#主页
	path('',views.index,name='index'),
	#显示所有主题
	path('systems/',views.systems, name='systems'),
	path('systems/<int:system_id>/',views.system, name='system'),
	path('new_system/',views.new_system, name='new_system'),
	path('edit_system/<int:system_id>/',views.edit_system, name='edit_system'),
	path('del_system/<int:system_id>/',views.del_system, name='del_system'),
	path('<int:system_id>/items/',views.items, name='items'),
	path('<int:system_id>/new_item/',views.new_item, name='new_item'),
	path('<int:system_id>/edit_item/<int:item_id>/',views.edit_item, name='edit_item'),
	path('<int:system_id>/del_item/<int:item_id>/',views.del_item, name='del_item'),
	path('<int:system_id>/formulars/',views.formulars, name='formulars'),
	path('<int:system_id>/new_formular/',views.new_formular, name='new_formular'),
	path('<int:system_id>/edit_formular/<int:formular_id>',views.edit_formular, name='edit_formular'),
	path('<int:system_id>/del_formular/<int:formular_id>',views.del_formular, name='del_formular'),
	
]
