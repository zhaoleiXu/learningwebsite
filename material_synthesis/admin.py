from django.contrib import admin

# Register your models here.
from .models import Msystem,Item,Formular,Reactant,Product
admin.site.register(Msystem)
admin.site.register(Item)
admin.site.register(Formular)
admin.site.register(Reactant)
admin.site.register(Product)