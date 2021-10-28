from django.contrib import admin
from .models import Stock,LookupStock,OHCL,News,Indices,OHCLI

# Register your models here.

admin.site.register(Stock)
admin.site.register(LookupStock)
admin.site.register(OHCL)
admin.site.register(News)
admin.site.register(Indices)
admin.site.register(OHCLI)


