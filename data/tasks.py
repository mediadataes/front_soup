import requests
from celery import shared_task
from django.shortcuts import get_object_or_404

from newspaper.models import Newspaper
from .models import Data


@shared_task
def download_url(pk, url):
    page = requests.get(url)
    content = page.content
    newspaper = get_object_or_404(Newspaper, pk=pk)
    data = Data(newspaper=newspaper, html=content)
    data.save()
    return data.pk
