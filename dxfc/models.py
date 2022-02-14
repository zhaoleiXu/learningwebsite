from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dimension(models.Model):
	"""维度，点需要的值称谓的描述，如x轴上值为3，x轴即是维度"""
	name = models.CharField('维度名',max_length=50)

class PointDims(models.Model):
	"""类似键值类型，多重复用，所以不独属于某点..."""
	dimension = models.CharField('维度',max_length=20)
	dim_value =models.DecimalField('值',max_digits=20,decimal_places=3,default=0)
		
class Point(models.Model):
	"""点可多维，不止二维 plane,为了普适，用维度暂代"""
	name = models.CharField('点名称',max_length=50)
	dims = models.ManyToManyField(PointDims)

class Line(models.Model):
	"""若干点定一线"""
	name = models.CharField('线名称',max_length=50)
	points = models.ManyToManyField(Point)

class shape(models.Model):
	"""若干线定一图形"""
	name = models.CharField('图形名称',max_length=50)
	lines = models.ManyToManyField(Line)
