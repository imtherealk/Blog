from django.contrib import admin
from blog.models import Categories, TagModel, Entries


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created',)

admin.site.register(Categories)
admin.site.register(TagModel)
admin.site.register(Entries, EntryAdmin)
