import os
import re
import requests
from celery import shared_task
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from newspaper.models import Newspaper
from .models import Data


def fix_lzld(save_dir):
    """ Some pages use attribute data-src or data-lzld-src with lazy load tools
    for load images, and other pages use srcset, these attributes contain images
    which aren't download with wget command """
    with open(os.path.join(save_dir, 'index.html'), 'r') as f:
        index = f.read()

    findall = re.findall('[ |"](//[\S]*.[jpg|png|jpeg])[ |"]', index)
    for url in findall:
        command = 'wget -P {} --no-use-server-timestamps -q {}'
        command = command.format(save_dir, url)
        os.popen(command)
        name = url.split('/')[-1]
        index.replace(url, name)
    with open(os.path.join(save_dir, 'index.html'), 'w') as f:
        f.write(index)


@shared_task
def download_url(pk, strtime, url):
    newspaper = get_object_or_404(Newspaper, pk=pk)
    now = timezone.now().strftime('%d-%m-%Y')
    path = '{}/{}/{}'.format(now, newspaper.name, strtime).replace(' ', '_')
    save_dir = os.path.join(settings.STATIC_ROOT, path)
    command = 'wget -nd -E -k -H -p -P {} -A jpg,svg,gif,png,html,woff,css,js --no-use-server-timestamps --restrict-file-names=windows -e robots=off -q {}'
    command = command.format(save_dir, url)
    os.popen(command)
    page = requests.get(url)
    content = page.text
    fix_lzld(save_dir)
    data = Data(newspaper=newspaper, path=path, html=content)
    data.save()
    return data.pk
