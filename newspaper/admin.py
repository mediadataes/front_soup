from django.contrib import admin

from .models import Newspaper


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'morning', 'afternoon', 'night', 'active')
    search_fields = ('name', 'url')
    list_filter = ('active',)
