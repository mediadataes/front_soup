from django.contrib import admin

from .models import Data


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('newspaper', 'created')
    search_fields = ('html', 'newspaper__name')
    list_filter = ('newspaper__name', 'created')
    #raw_id_fields = ('newspaper',)
