from django.test import Client, TestCase
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from data.models import Data
from data.tasks import download_url
from .models import Newspaper


class NewspaperTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.np = Newspaper(name='El diario', url='https://www.eldiario.es/')
        self.np.save()
        self.np_disabled = Newspaper(name='El diario 2',
                                     url='https://www.eldiario2.es/',
                                     active=False)
        self.np_disabled.save()

    def test_print_newspaper(self):
        name = 'El pais'
        newspaper = Newspaper(name=name, url='https://elpais.com/')
        newspaper.save()
        self.assertEqual(str(newspaper), name)

    def test_create_newspaper(self):
        start_pt = PeriodicTask.objects.count()
        newspaper = Newspaper(name='El pais', url='https://elpais.com/')
        newspaper.save()
        end_pt = PeriodicTask.objects.count()
        self.assertEqual(end_pt - start_pt, 3)

    def test_create_newspaper_disabled(self):
        start_pt = PeriodicTask.objects.count()
        newspaper = Newspaper(name='El pais',
                              url='https://elpais.com/',
                              active=False)
        newspaper.save()
        end_pt = PeriodicTask.objects.count()
        self.assertEqual(end_pt - start_pt, 0)

    def test_edit_newspaper_url(self):
        start_pt = PeriodicTask.objects.count()
        self.np.url = 'https://test.com'
        self.np.save()
        end_pt = PeriodicTask.objects.count()
        self.assertEqual(end_pt - start_pt, 0)

    def test_disabled_newspaper(self):
        start_pt = PeriodicTask.objects.count()
        self.np.active = False
        self.np.save()
        end_pt = PeriodicTask.objects.count()
        self.assertEqual(end_pt - start_pt, -3)

    def test_enable_newspaper(self):
        start_pt = PeriodicTask.objects.count()
        self.np_disabled.active = True
        self.np_disabled.save()
        end_pt = PeriodicTask.objects.count()
        self.assertEqual(end_pt - start_pt, 3)

    def test_rm_newspaper(self):
        start_pt = PeriodicTask.objects.count()
        self.np.delete()
        end_pt = PeriodicTask.objects.count()
        self.assertEqual(end_pt - start_pt, -3)

    def test_task_download(self):
        start_data = Data.objects.count()
        download_url(self.np.pk, self.np.url)
        end_data = Data.objects.count()
        self.assertEqual(end_data - start_data, 1)
