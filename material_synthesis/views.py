from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator
from .models import Msystem,Item,Formular,Reactant,Product
from .forms import MsystemForm,ItemForm,FormularForm,ReactantForm,ProductForm
# Create your views here.
def index(request):
	"""材料合成的主页"""
	return render(request, 'material_synthesis/index.html')

@login_required
def systems(request):
	"""显示所有主题"""
	systems = Msystem.objects.filter(owner=request.user).order_by('date_added')
	context = {'systems': systems}
	return render(request, 'material_synthesis/systems.html',context)

@login_required
def system(request, system_id):
	"""显示特定主题及其条目"""
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404
	context = {'system':msystem}
	return render(request, 'material_synthesis/system.html',context)


@login_required
def new_system(request):
	"""添加新合成系统"""
	if request.method != 'POST':
		#未提交数据： 创建一个新表单
		form = MsystemForm()
	else:
		#POST 提交的数据：处理
		form = MsystemForm(data=request.POST)
		if form.is_valid():
			new_system = form.save(commit=False)
			new_system.owner = request.user
			new_system.save()
			return redirect('material_synthesis:systems')
	# 显示空表单或指出表单数据无效
	context = {'form':form}
	return render(request, 'material_synthesis/new_system.html',context)

@login_required
def edit_system(request,system_id):
	"""编辑系统名称"""
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404

	if request.method != 'POST':
		#未提交数据： 创建一个新表单
		form = MsystemForm(instance=msystem)
	else:
		#POST 提交的数据：处理
		form = MsystemForm(instance=msystem,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('material_synthesis:system',system_id=msystem.id)
	# 显示空表单或指出表单数据无效
	context = {'form':form,'system':msystem}
	return render(request, 'material_synthesis/edit_system.html',context)

@login_required
def del_system(request,system_id):
	"""删除系统，数据将级联删除"""
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404

	if msystem:
		msystem.delete()

	return redirect('material_synthesis:systems')


@login_required
def items(request,system_id):
	"""显示所有材料"""
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404
	items = Item.objects.filter(msystem=msystem).order_by('date_added')
	
	cur_page = int(request.GET.get('page',1))
	count = request.GET.get('count',15)
	paginator = Paginator(items,count)
	if cur_page > paginator.num_pages:
		cur_page = 1
	page = paginator.page(cur_page)
	# 使用了分页功能，items替换成page
	context = {'page': page,'system':msystem,'count':count}
	return render(request, 'material_synthesis/items.html',context)


@login_required
def new_item(request,system_id):
	"""系统添加新材料"""
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# 未提交数据：创建一个空表单
		form = ItemForm()
	else:
		# POST提交的数据：处理
		form = ItemForm(data=request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.msystem = msystem
			new_item.save()
			return redirect('material_synthesis:items', system_id = system_id)
	
	#显示空表单或指出表单数据无效
	context = {'system':msystem,'form':form}
	return render(request, 'material_synthesis/new_item.html',context)

@login_required
def edit_item(request,system_id,item_id):
	"""编辑特定材料"""
	item = Item.objects.get(id=item_id)
	msystem = item.msystem
	if msystem.owner != request.user or msystem.id != system_id:
		raise Http404
	
	if request.method != 'POST':
		# 初次请求：  使用当前条目填充表单
		form = ItemForm(instance=item)
	else:
		# POST 提交的数据： 处理
		form = ItemForm(instance=item, data= request.POST)
		if form.is_valid():
			form.save()
			return redirect('material_synthesis:items', system_id = system_id)
	
	context = {'system':msystem,'form':form,'item_id':item_id}
	return render(request, 'material_synthesis/edit_item.html', context)

@login_required
def del_item(request,system_id,item_id):
	"""删除系统，数据将级联删除"""
	item = Item.objects.get(id=item_id)
	msystem = item.msystem
	if msystem.owner != request.user or msystem.id != system_id:
		raise Http404

	if item:
		item.delete()

	return redirect('material_synthesis:items',system_id=system_id)

@login_required
def formulars(request,system_id):
	'''查看所有反应方程式'''
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404
	default_reactants = msystem.default_reactants
	default_products = msystem.default_products
	formulars = Formular.objects.filter(msystem=msystem).order_by('date_added')

	cur_page = int(request.GET.get('page',1))
	count = request.GET.get('count',15)
	paginator = Paginator(formulars,count)
	if cur_page > paginator.num_pages:
		cur_page = 1
	page = paginator.page(cur_page)
	# 使用了分页功能，formular替换成page
	context = {'page': page,'system':msystem,'count':count,'default_reactants':default_reactants,
		'default_products':default_products}
	return render(request, 'material_synthesis/formulars.html',context)

from django.forms import formset_factory
@login_required
def new_formular(request,system_id):
	"""系统添加新材料"""
	msystem = Msystem.objects.get(id=system_id)
	if msystem.owner != request.user:
		raise Http404
	# 修改反应生成物种类获取从页面获得，若无再用默认值
	default_reactants = request.GET.get('reactants',msystem.default_reactants)
	default_products = request.GET.get('products',msystem.default_products)
	default_reactants = int(default_reactants)
	default_products = int(default_products)

	ReactantFormSet = formset_factory(ReactantForm,extra=default_reactants)
	# ProductFormSet = formset_factory(ProductForm,max_num=default_products,extra=3)
	ProductFormSet = formset_factory(ProductForm,extra=default_products)
	if request.method != 'POST':
		# 未提交数据：创建一个空表单
		form = FormularForm()
		# 添加的表单关键字传参貌似传到了每个实例上
		reactantformset = ReactantFormSet(form_kwargs={'msystem':msystem},prefix='reactants')
		productformset = ProductFormSet(form_kwargs={'msystem':msystem},prefix='products')
	else:
		# POST提交的数据：处理
		form = FormularForm(data=request.POST)
		reactantformset = ReactantFormSet(data=request.POST,form_kwargs={'msystem':msystem},prefix='reactants')
		productformset = ProductFormSet(data=request.POST,form_kwargs={'msystem':msystem},prefix='products')
		if form.is_valid():
			new_formular = form.save(commit=False)
			new_formular.msystem = msystem
			new_formular.save()
			for reactantform in reactantformset:
				if reactantform.is_valid():
					reactants = reactantform.save(commit=False)
					if reactants.item_id is None:
						continue
					reactants.formular = new_formular
					reactants.save()
			for productform in productformset:
				if productform.is_valid():
					products = productform.save(commit=False)
					if products.item_id is None:
						continue
					products.formular = new_formular
					products.save()
			return redirect('material_synthesis:formulars', system_id = system_id)
	
	#显示空表单或指出表单数据无效
	context = {'system':msystem,'form':form,'reactantformset':reactantformset,'productformset':productformset}
	return render(request, 'material_synthesis/new_formular.html',context)

from django.forms import inlineformset_factory
@login_required
def edit_formular(request,system_id,formular_id):
	"""系统添加新材料"""
	msystem = Msystem.objects.get(id=system_id)
	formular = Formular.objects.get(id=formular_id)
	if msystem.owner != request.user or formular.msystem != msystem:
		raise Http404

	ReactantFormSet = inlineformset_factory(Formular,Reactant,fields=('item','amount'),extra=1)
	ProductFormSet = inlineformset_factory(Formular,Product,fields=('item','amount'),extra=1)

	# 以下注释代码的max_num 显示共计5项表单内容
	# ReactantFormSet = inlineformset_factory(Formular,Reactant,fields=('item','amount'),max_num=msystem.maxno_reactants)
	# ProductFormSet = inlineformset_factory(Formular,Product,fields=('item','amount'),max_num=msystem.maxno_products)

	# 以下是使用 formset_factory的部分初始化显示代码，更新inline后不用
	# reactdata = []
	# reactants = Reactant.objects.filter(formular=formular)
	# for item in reactants:
	# 	reactdata.append({'item':item.item_id,'amount':item.amount})

	# proddata =[]
	# products = Product.objects.filter(formular=formular)
	# for item in products:
	# 	proddata.append({'item':item.item_id,'amount':item.amount})

	if request.method != 'POST':
		# 未提交数据：创建一个空表单
		form = FormularForm(instance=formular)
		# 添加的表单关键字传参貌似传到了每个实例上
		
		reactantformset = ReactantFormSet(instance=formular,prefix='reactants')
		productformset = ProductFormSet(instance=formular,prefix='products')

		# reactantformset = ReactantFormSet(initial=reactdata,form_kwargs={'msystem':msystem},prefix='reactants')
		# productformset = ProductFormSet(initial=proddata,form_kwargs={'msystem':msystem},prefix='products')
	else:
		# POST提交的数据：处理
		form = FormularForm(instance= formular,data=request.POST)
		# 以下注释为使用formset_factory的代码
		# reactantformset = ReactantFormSet(data=request.POST,form_kwargs={'msystem':msystem},prefix='reactants')
		# productformset = ProductFormSet(data=request.POST,form_kwargs={'msystem':msystem},prefix='products')
		if form.is_valid():
			edit_formular = form.save(commit=False)
			edit_formular.msystem = msystem
			edit_formular.save()
			reactantformset = ReactantFormSet(request.POST,instance= edit_formular,prefix='reactants')
			if reactantformset.is_valid():
				reactantformset.save()
			productformset = ProductFormSet(request.POST,instance = edit_formular,prefix='products')
			if productformset.is_valid:
				productformset.save()

			# 以下注释为使用formset_factory的代码，但更新困难，新旧变化对比、删除、更新麻烦
			# for reactantform in reactantformset:
			# 	if reactantform.is_valid():
			# 		reactant = reactantform.save(commit=False)
			# 		if reactant.item_id is None:
			# 			continue
			# 		old_reactant = reactants.get(item_id=reactant.item_id)
			# 		if old_reactant:
			# 			old_reactant.amount = reactant.amount
			# 			old_reactant.save()
			# 		reactant.formular = edit_formular
			# 		reactant.save()
			# for productform in productformset:
			# 	if productform.is_valid():
			# 		product = productform.save(commit=False)
			# 		if product.item_id is None:
			# 			continue
			# 		product.formular = edit_formular
			# 		product.save()
			return redirect('material_synthesis:formulars', system_id = system_id)
	
	#显示空表单或指出表单数据无效
	context = {'system':msystem,'formular':formular,'form':form,'reactantformset':reactantformset,'productformset':productformset}
	return render(request, 'material_synthesis/edit_formular.html',context)

@login_required
def del_formular(request,system_id,formular_id):
	"""系统添加新材料"""
	msystem = Msystem.objects.get(id=system_id)
	formular = Formular.objects.get(id=formular_id)
	if msystem.owner != request.user or formular.msystem != msystem:
		raise Http404
	# formular.f_reactants.clear()
	# formular.f_products.clear()
	formular.delete()
	return redirect('material_synthesis:formulars', system_id = system_id)
	