from django.shortcuts import render
from django.http import HttpResponse
from . import models as mathmodel

# Create your views here.
def homepage(request):
	print(request.path_info)
	return render(request,"dxfc/index.html")

def add_dimension(request):
	if request.method == 'GET':
		value = request.GET.get('dimension','')
		if value != '':
			dim = mathmodel.Dimension.objects.create(name=value)
			return HttpResponse("Dimension added.")
	elif request.method =='POST':
		value = request.POST.get('dimension','')
		if value != '':
			dim = mathmodel.Dimension.objects.create(name=value)
			return HttpResponse("Dimension added.")

	return render(request,'dxfc/add_dimension.html')

def list_dimension(request):
	dims = mathmodel.Dimension.objects.all()
	return render(request,'dxfc/list_dimension.html',locals())

def del_dimension(request,id):
	try:
		dim = mathmodel.Dimension.objects.get(id=id)
		if dim is not None:
			dim.delete()
	except Exception as e:
		return HttpResponse("failed.")
	return redirect('/dxfc/dimension/list')

def modify_dimension(request,id):
	try:
		dim = mathmodel.Dimension.objects.get(id=id)
		if dim is not None:
			if request.method == "GET":
				return render(request,'dxfc/edit_dimension.html',locals())
			elif request.method == "POST":
				dim.name = request.POST.get("dimension",dim.name)
				dim.save()
	except Exception as e:
		return HttpResponse("modify failed")
	return redirect('/dxfc/dimension/list')
