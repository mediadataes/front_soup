from import_export import resources
from .models import Newspaper


class NewspaperResource(resources.ModelResource):
    class Meta:
        model = Newspaper
        fields = ('name', 'url')
        import_id_fields = ('url',)
