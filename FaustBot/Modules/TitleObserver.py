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
        url = re.search(regex, data["messageCaseSensitive"])
        if url is not None:
            url = url.group()
            print(url)
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                }

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
        url = resource.geturl()
        # der erste Fall kann raus, wenn ein anderer Channel benutzt wird
        if url.find("rehakids.de") != -1:
            encoding = "windows-1252"
        if not encoding:
            encoding = "utf-8"
        content = resource.read().decode(encoding, errors="replace")

        if re.search("http[s]+://[^/]*youtube.com/", url):
            title_re = re.compile(
                '''"results":{"contents":\[{"videoPrimaryInfoRenderer":{"title":{"runs":\[{"text":"([^"]*)"'''
            )
        else:
            title_re = re.compile("<title>(.+?)</title>")

        title_matches = title_re.search(content)
        if title_matches:
            title = title_matches.group(1)
        else:
            return "Could not Parse Title"

        title = html.unescape(title)
        title = title.replace("\n", " ").replace("\r", "")
        title = title.replace("&lt;", "<")
        title = title.replace("&gt;", ">")
        title = title.replace("&amp;", "&")
        if title == "":
            title = "Empty Title"
        return title
