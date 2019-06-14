from factory.django import DjangoModelFactory
from factory import SubFactory

from .models import Newspaper


class NewspaperFactory(DjangoModelFactory):

    class Meta:
        model = Newspaper
