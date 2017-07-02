from ..settings import Config
import requests, urllib.parse, json

class API():
    def __init__(self, long_link):
        self._long_link = long_link
        self._short_links = []
        self._post_data = {'longUrl': long_link}
        self.count = 0

    def add_link(self, site_name, link):
        self._short_links.append((site_name, link))
        self.count += 1
        return

    # goo.gl
    def googl(self):
        if Config.googl is not None:
            content = requests.post(
                "https://www.googleapis.com/urlshortener/v1/url?key={0}".format(Config.googl, ),
                json=self._post_data)
        else:
            content = requests.post('https://www.googleapis.com/urlshortener/v1/url', json=self._post_data)
        if (content.status_code == 200):
            j = json.loads(content.text)
            self.add_link('goo.gl', j['id'])
            return True
        return False

    # bit.ly
    def bitly(self):
        # Requires API Key
        if Config.bitly is None:
            return False
        content = requests.get(
            "https://api-ssl.bitly.com/v3/shorten/?access_token={0}&longUrl={1}".format(Config.bitly,
                                                                                        urllib.parse.quote(self._long_link,
                                                                                                           safe=''), ))
        if (content.status_code == 200):
            j = json.loads(content.text)
            if (j['status_txt'] == 'OK'):
                self.add_link('bit.ly', j['data']['url'])
                return True
        return False

    # tinyurl.com
    def tinyurl(self):
        if not Config.tinyurl:
            return False
        content = requests.post("http://tinyurl.com/api-create.php?url={0}".format(urllib.parse.quote(self._long_link,safe=''), ))
        if (content.status_code == 200):
            self.add_link('tinyurl.com', content.text)
            return True
        return False
