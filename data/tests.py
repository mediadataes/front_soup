from django.test import Client, TestCase
from parameterized import parameterized

from .factories import DataFactory
from .models import Data


class DataTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        with open('data/example.html', 'r') as html_file:
            html = html_file.read()
        self.data = DataFactory.create(html=html)

    @parameterized.expand([
        ('title', 2),
        ('subtitle', 1),
        ('Lorem Ipsum', 5),
        ('electronic', 1),
        ('version', 2),
        ('siesta', 0),
        ('cigüeña', 1),
        ('camión', 1),
        ('me', 0),

    ])
    def test_search_elements(self, text, result):
        elements = self.data.get_text_parts_that_contain(text)
        self.assertEqual(len(elements), result)
