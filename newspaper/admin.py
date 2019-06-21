from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Newspaper
from .resources import NewspaperResource


@admin.register(Newspaper)
class NewspaperAdmin(ImportExportModelAdmin):
    list_display = ('name', 'url', 'morning', 'afternoon', 'night', 'active')
    search_fields = ('name', 'url')
    list_filter = ('active',)
    resource_class = NewspaperResource
