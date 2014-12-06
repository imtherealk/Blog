from django.contrib import admin
from blog.models import *

class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'Title', 'created',)

admin.site.register(Categories)
admin.site.register(TagModel)
admin.site.register(Entries, EntryAdmin)
