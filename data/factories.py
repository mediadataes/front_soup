from factory.django import DjangoModelFactory
from factory import SubFactory

from newspaper.factories import NewspaperFactory
from .models import Data


class DataFactory(DjangoModelFactory):
    newspaper = SubFactory(NewspaperFactory)

    class Meta:
        model = Data
