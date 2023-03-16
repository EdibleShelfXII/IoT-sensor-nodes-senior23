from django.contrib import admin

from .models import Question, Hub, Node, Data

admin.site.register(Question)
admin.site.register(Hub)
admin.site.register(Node)
admin.site.register(Data)

