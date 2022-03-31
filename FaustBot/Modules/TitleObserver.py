import html
import re
import urllib
from urllib import request

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class TitleObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        regex = "(?P<url>https?://[^\s]+)"
        url = re.search(regex, data['message'])
        if url is not None:
            url = url.group()
            print(url)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                url = url
                req = urllib.request.Request(url, None, headers)
                resource = urllib.request.urlopen(req)
                title = self.getTitle(resource)
                print(title)
                title = title[:350]
                connection.send_back(title, data)
            except Exception as exc:
                print(exc)
                pass
            
    def getTitle(self, resource):
            encoding = resource.headers.get_content_charset()
            # der erste Fall kann raus, wenn ein anderer Channel benutzt wird
            if resource.geturl().find('rehakids.de') != -1:
                encoding = 'windows-1252'
            if not encoding:
                encoding = 'utf-8'
            content = resource.read().decode(encoding, errors='replace')
            title_re = re.compile("<title>(.+?)</title>")
            title = title_re.search(content).group(1)
            title = html.unescape(title)
            title = title.replace('\n', ' ').replace('\r', '')
            title = title.replace("&lt;", "<")
            title = title.replace("&gt;", ">")
            title = title.replace("&amp;", "&")
            return title
