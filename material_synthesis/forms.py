from django import forms
from django.core.exceptions import ValidationError

from .models import Msystem,Item,Formular,Reactant,Product

class MsystemForm(forms.ModelForm):
	class Meta:
		model = Msystem
		fields = ['text','maxno_reactants','maxno_products']
		labels = {'text': '材料合成体系名称','maxno_reactants':'方程式反应物最大种类数','maxno_products':'方程式生成物最大种类数'}

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name','selling_price','purchase_price','timecost','production_rate','stock','unit_measure','introduction']
		labels = {'name': '*材料唯一名','production_rate':'生产速度（计量单位/秒）','unit_measure':'计量单位','introduction':'简介'}
		widgets = {'introduction': forms.Textarea(attrs={'cols':80})}

class FormularForm(forms.ModelForm):
	class Meta:
		model = Formular
		fields = ['name','timecost','introduction']
		labels = {'name': '*反应式唯一名','timecost':'反应耗时','introduction':'简介'}
		widgets = {'introduction': forms.Textarea(attrs={'cols':80})}

class ReactantForm(forms.ModelForm):
	"""反应物表单，主要用于表单集"""
	class Meta:
		model = Reactant
		fields = ['item','amount']
		labels = {}

	def __init__(self,*args,**kwargs):
		# 从参数中获取体系参数，并只显示本体系的item列表，参考网文+调试1天终于正确地控制了
		self.msystem = kwargs.pop('msystem')
		super(ReactantForm,self).__init__(*args,**kwargs)
		self.fields['item'] = forms.ModelChoiceField(
			queryset = Item.objects.filter(msystem=self.msystem)
			)

	def clean_item(self):
		item = self.cleaned_data['item']

		if item is None :
			raise ValidationError(_('item id null'))
		return item

	def cleaned_amount(self):
		amount = self.cleaned_data['amount']
		if amount == 0:
			raise ValidationError(_('item amont 0'))
		return amount

class ProductForm(forms.ModelForm):
	"""反应物表单，主要用于表单集"""
	class Meta:
		model = Product
		fields = ['item','amount']
		labels = {}

	def __init__(self,*args,**kwargs):
		# 从参数中获取体系参数，并只显示本体系的item列表，参考网文+调试1天终于正确地控制了
		self.msystem = kwargs.pop('msystem')
		super(ProductForm,self).__init__(*args,**kwargs)
		self.fields['item'] = forms.ModelChoiceField(
			queryset = Item.objects.filter(msystem=self.msystem)
			)

	def clean_item(self):
		item = self.cleaned_data['item']

		if item is None :
			raise ValidationError(_('item id null'))
		return item

	def cleaned_amount(self):
		amount = self.cleaned_data['amount']
		if amount == 0:
			raise ValidationError(_('item amont 0'))
		return amount
		