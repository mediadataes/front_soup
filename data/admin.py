import os
import zipfile
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse
from io import BytesIO

from .models import Data


def download_datas(modeladmin, request, queryset):
    """ Actions that create a buffer and add html files to zip """
    buffer = BytesIO()
    zip = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED)
    gen = datetime.now().isoformat()
    if not queryset:
        queryset = Data.objects.all()
    for data in queryset:
        newspaper = data.newspaper.name
        date = data.created.strftime('%d-%m-%Y')
        path = '/tmp/{}/{}/{}/'.format(gen, date, newspaper)
        os.makedirs(path, exist_ok=True)
        filename = data.created.strftime('%H:%M.html')
        full_path = os.path.join(path, filename)
        zip.writestr(full_path, data.html)
    zip.close()

    buffer.flush()
    result = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename=datas.zip'
    response.write(result)
    return response
download_datas.short_description = "Download .zip"


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('newspaper', 'created')
    search_fields = ('html', 'newspaper__name')
    list_filter = ('newspaper__name', 'created')
    actions = [download_datas]
    current_query = ''

    def get_changelist_instance(self, request):
        # My override part for adding new column if exist a query
        query = request.GET.dict().get('q')
        if query and len(query) >= 3:
            self.current_query = query[:]
            list_display = ('newspaper', 'created', 'get_search_text')
        else:
            list_display = ('newspaper', 'created')
        # Django code
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        if self.get_actions(request):
            list_display = ['action_checkbox', *list_display]
        sortable_by = self.get_sortable_by(request)
        ChangeList = self.get_changelist(request)
        return ChangeList(
            request,
            self.model,
            list_display,
            list_display_links,
            self.get_list_filter(request),
            self.date_hierarchy,
            self.get_search_fields(request),
            self.get_list_select_related(request),
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            sortable_by,
        )

    def get_search_text(self, obj):
        if not self.current_query:
            return
        founds = obj.get_text_parts_that_contain(self.current_query)
        return '{} resultados\n {}'.format(len(founds), '\n'.join(founds))

    class Media:
        css = {'all': ('data/data-admin.css',)}

    get_search_text.short_description = 'Found'
