from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from . import models, apps, utils, settings
from .models import Link

from .templates.api import API

# Create your views here.

def index(request):
    return render(request, 'index.html')

def history(request):
    ip = utils.get_client_ip(request)
    return render(request, 'history.html', {'links': Link.objects.filter(ip=ip)})

def short_link(request):
    if (request.method != "POST" and request.method != "GET"):
        return render(request, 'index.html', {'error': 'Invalid Request'})
    if (request.method == "GET"):
        if ('link' not in request.GET or request.GET['link'] is None):
            return render(request, 'index.html', {'error': 'Invalid Request'})
        l = request.GET['link']
    elif (request.method == "POST"):
        if (not ('link' in request.POST and request.POST['link'])):
            return render(request, 'index.html', {'error': 'Invalid Request'})
        l = request.POST['link']

    if (len(l) > 200):
        return render(request, 'index.html', {'error': 'Link is too long'})
    val = URLValidator()
    try:
        val(l)
    except (ValidationError):
        return render(request, 'index.html', {'error': 'Invalid Link Format'})

    ip = utils.get_client_ip(request)

    api = API(l)
    # goo.gl
    api.googl()
    # bit.ly
    api.bitly()
    # tinyurl.com
    api.tinyurl()

    dblink = models.Link.create(l, api._short_links, ip)
    if api.count == 0:
        return render(request, 'index.html', {'error': 'No API Found to convert into short links'})
    return render(request, 'index.html', {'links': api._short_links, 'long_url': l})