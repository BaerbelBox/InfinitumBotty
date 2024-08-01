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
                title = self.getTitle(url)
                print(title)
                title = title[:350]
                connection.send_back(title, data)
            except Exception as exc:
                print(exc)
                pass

    def getTitle(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        if re.search("https?://\\[[^/]*", url):
            raise (Exception("Refusing to parse bare IPv6 Addresses"))
        if re.search("https?://[^/:]*:[^/:]*", url):
            raise (Exception("Refusing to parse URLs with Ports"))
        if re.search("https?://[0-9]+.[0-9]+.[0-9]+.[^/]*", url):
            raise (Exception("Refusing to parse bare IPv4 Addresses"))
        if re.search("https?://music.youtube.com/", url):
            url = url.replace("music.youtube.com/", "www.youtube.com/", 1)

        if re.search("https?://[^/]*youtube.com/shorts/", url):
            title_re = re.compile('''"reelPlayerHeaderRenderer":{"reelTitleText":{"runs":\[{"text":"([^"]*)"''')
            headers["User-Agent"] = "curl/7.81.0"
        elif re.search("https?://[^/]*youtube.com/", url):
            title_re = re.compile(
                '''"results":{"contents":\[{"videoPrimaryInfoRenderer":{"title":{"runs":\[{"text":"([^"]*)"'''
            )
        else:
            title_re = re.compile("<title>(.+?)</title>")

        req = urllib.request.Request(url, None, headers)

        # Keep the urlopen scope as short as possible (connection leaks)
        with urllib.request.urlopen(req, timeout=10) as response:
            encoding = response.headers.get_content_charset()
            content_raw = response.read()

        # der erste Fall kann raus, wenn ein anderer Channel benutzt wird
        if url.find("rehakids.de") != -1:
            encoding = "windows-1252"
        if not encoding:
            encoding = "utf-8"

        content = content_raw.decode(encoding, errors="replace")

        title_matches = title_re.search(content)
        if title_matches:
            title = title_matches.group(1)
        else:
            #with open("content.html", "w") as file:
            #    file.write(content)
            raise Exception("Could not Parse Title for {}".format(url))

        title = html.unescape(title)
        title = title.replace("\n", " ").replace("\r", "")
        title = title.replace("&lt;", "<")
        title = title.replace("&gt;", ">")
        title = title.replace("&amp;", "&")
        if title == "":
            raise Exception("Empty Title for {}".format(url))
        return title
