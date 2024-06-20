from django.contrib import admin

from dating.models import CodeSnippet, Location, Opinion, Message

# Register your models here.
admin.site.register(CodeSnippet)
admin.site.register(Location)
admin.site.register(Opinion)
admin.site.register(Message)

