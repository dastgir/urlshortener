from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    name = 'shortener'
    # API Keys
    # goo.gl API Key (https://developers.google.com/url-shortener/v1/getting_started)
    googl = ''
    # bit.ly API Key
    bitly = ''
