from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Msystem(models.Model):
	"""材料合成系统名称，允许用户创建多套系统"""
	text = models.CharField(max_length=200)
	default_reactants = models.IntegerField(default=5)
	default_products = models.IntegerField(default=5)
	maxno_reactants = models.IntegerField(default=5)
	maxno_products = models.IntegerField(default=5)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		"""返回模型的字符串表示"""
		return self.text

class Item(models.Model):
	"""特定合成系统的具体材料"""
	msystem = models.ForeignKey(Msystem,on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	selling_price = models.DecimalField('售价',max_digits=30,decimal_places=4,default=0)
	purchase_price = models.DecimalField('进价',max_digits=30,decimal_places=4,default=0)
	timecost = models.DecimalField('耗秒',max_digits=30,decimal_places=7,default=0)
	production_rate = models.DecimalField('产速（个/秒）',max_digits=30,decimal_places=7,default=0)
	stock = models.DecimalField('当前存量',max_digits=30,decimal_places=7,default=0)
	unit_measure = models.CharField(max_length=30,default='',blank=True)
	introduction = models.TextField(default='',blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name_plural = 'items'
	
	def __str__(self):
		"""返回模型的字符串表示"""
		
		return self.name

class Formular(models.Model):
	"""合成公式及概述（含条件）"""
	msystem = models.ForeignKey(Msystem,on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	timecost = models.DecimalField('耗秒',max_digits=30,decimal_places=7,default=0)

	f_reactants = models.ManyToManyField(Item,through='Reactant',related_name='reactants')
	f_products = models.ManyToManyField(Item,through='Product',related_name='products')
	introduction = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name_plural = 'formulars'
	
	def __str__(self):
		"""返回模型的字符串表示"""
		
		return self.name + ' : ' + self.introduction[:50] + "..."

class Reactant(models.Model):
	"""反应物及量"""
	formular = models.ForeignKey(Formular,on_delete=models.CASCADE)
	item = models.ForeignKey(Item,on_delete=models.CASCADE)
	amount = models.DecimalField('消耗数量',max_digits=30,decimal_places=7,default=0)

	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name_plural = 'reactants'
	
	def __str__(self):
		"""返回模型的字符串表示"""
		
		return self.formular.name + ':' + self.item.name + ' : ' + str(self.amount)

class Product(models.Model):
	"""生成物及量"""
	formular = models.ForeignKey(Formular,on_delete=models.CASCADE)
	item = models.ForeignKey(Item,on_delete=models.CASCADE)
	amount = models.DecimalField('生成数量',max_digits=30,decimal_places=7,default=0)

	date_added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name_plural = 'products'
	
	def __str__(self):
		"""返回模型的字符串表示"""
		
		return self.formular.name + ':' + self.item.name + ' : ' + str(self.amount)
