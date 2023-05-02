from django.contrib import admin

from .models import Hub, Node, Data

admin.site.register(Hub)
admin.site.register(Node)
admin.site.register(Data)

