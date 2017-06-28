from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from . import models, apps, utils
import requests, urllib.parse, json

# Create your views here.

def index(request):
    return HttpResponse("Please refer to documentation.")

def short_link(request):
    if (request.method != "POST" and request.method != "GET"):
        return HttpResponse("Invalid Request")
    if (request.method == "GET"):
        if ('link' not in request.GET or request.GET['link'] is None):
            return HttpResponse("Invalid Request")
        l = request.GET['link']
    else:
        if (not (request.data and request.data['link'])):
            return HttpResponse("Invalid Request")
        l = request.data['link']

    if (len(l) > 200):
        return HttpResponse("Size > 200")
    val = URLValidator()
    try:
        val(l)
    except (ValidationError):
        return HttpResponse("Invalid Link")

    ip = utils.get_client_ip(request)

    short_links = []
    # goo.gl
    post_data = {'longUrl': l}
    if apps.ShortenerConfig.googl is not None:
        content = requests.post("https://www.googleapis.com/urlshortener/v1/url?key={0}" .format(apps.ShortenerConfig.googl), json=post_data)
    else:
        content = requests.post('https://www.googleapis.com/urlshortener/v1/url', json=post_data)
    if (content.status_code == 200):
        j = json.loads(content.text)
        short_links.append(j['id'])
    print(content.text)
    # bit.ly
    if apps.ShortenerConfig.bitly is not None:
        content = requests.get("https://api-ssl.bitly.com/v3/shorten/?access_token={0}&longUrl={1}".format(apps.ShortenerConfig.bitly, urllib.parse.quote(l, safe='')))
        if (content.status_code == 200):
            j = json.loads(content.text)
            if (j['status_txt'] == 'OK'):
                short_links.append(j['data']['url'])

    print(short_links)
    dblink = models.Link.create(l, short_links, ip)
    return HttpResponse('Success: {0}'.format(':'.join(short_links)))