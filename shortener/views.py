from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from . import models, apps, utils
import requests, urllib.parse, json

# Create your views here.

def index(request):
    return render(request, 'index.html')

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

    short_links = []
    # goo.gl
    post_data = {'longUrl': l}
    if apps.ShortenerConfig.googl is not None:
        content = requests.post("https://www.googleapis.com/urlshortener/v1/url?key={0}" .format(apps.ShortenerConfig.googl,), json=post_data)
    else:
        content = requests.post('https://www.googleapis.com/urlshortener/v1/url', json=post_data)
    if (content.status_code == 200):
        j = json.loads(content.text)
        short_links.append(('goo.gl', j['id']))
    # bit.ly
    if apps.ShortenerConfig.bitly is not None:
        content = requests.get("https://api-ssl.bitly.com/v3/shorten/?access_token={0}&longUrl={1}".format(apps.ShortenerConfig.bitly, urllib.parse.quote(l, safe=''),))
        if (content.status_code == 200):
            j = json.loads(content.text)
            if (j['status_txt'] == 'OK'):
                short_links.append(('bit.ly', j['data']['url']))

    dblink = models.Link.create(l, short_links, ip)
    if not short_links:
        return render(request, 'index.html', {'error': 'No API Found to convert into short links'})
    return render(request, 'index.html', {'links': short_links, 'long_url': l})