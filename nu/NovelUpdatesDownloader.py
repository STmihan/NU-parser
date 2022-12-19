import random
import time
from pathlib import Path

import requests
import requests as Requests
from fake_headers import Headers

import Config
from nu.types import Novel


def _get_sleep_time():
    return random.randrange(Config.SLEEP_MIN, Config.SLEEP_MAX)


class NovelUpdatesDownloader:
    def __init__(self):
        Path(Config.SEARCH_HTML_PATH).mkdir(parents=True, exist_ok=True)
        Path(Config.NOVELS_HTML_PATH).mkdir(parents=True, exist_ok=True)
        Path(Config.CHAPTERS_HTML_PATH).mkdir(parents=True, exist_ok=True)

    def get_search_html(self, page, force=False):
        if not str(page).isdigit() or int(page) < 1:
            return Exception("Invalid page number")
        page = str(page)
        path = Config.SEARCH_HTML_PATH + page + ".html"
        if not Path(path).exists() or force:
            self._download_html(page)
            time.sleep(_get_sleep_time())

        html = self._open_file(path)
        return html

    def get_novel_html(self, novel: Novel, force=False):
        title = Novel.getNormalizedTitle(novel)
        path = Config.NOVELS_HTML_PATH + title + ".html"
        if not Path(path).exists() or force:
            self._download_novel_html(novel)
            time.sleep(_get_sleep_time())

        html = self._open_file(path)
        return html

    def get_novel_chapter_html(self, novel, novel_id, force=False):
        path = Config.CHAPTERS_HTML_PATH + Novel.getNormalizedTitle(novel) + ".html"
        if not Path(path).exists() or Path(path).stat().st_size == 0 or force:
            self._download_novel_chapter(novel, novel_id)
            time.sleep(_get_sleep_time())

        html = self._open_file(path)

        return html

    def _open_file(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def _download_html(self, page):
        page = str(page)
        headers_generator = Headers(
            browser="chrome",
            os="win",
            headers=False
        )
        headers = headers_generator.generate()

        response = Requests.get(
            url=Config.URL + page,
            headers=headers,
        )
        response.encoding = "utf-8"

        html = response.text
        with open(Config.SEARCH_HTML_PATH + page + ".html", "w", encoding="utf-8") as file:
            file.write(html)
        return html

    def _download_novel_html(self, novel: Novel):
        headers_generator = Headers(
            browser="chrome",
            os="win",
            headers=False
        )
        headers = headers_generator.generate()

        response = Requests.get(
            url=novel.link,
            headers=headers,
        )
        response.encoding = "utf-8"

        html = response.text
        local_html_path = Config.NOVELS_HTML_PATH + Novel.getNormalizedTitle(novel) + ".html"
        with open(local_html_path, "w+", encoding="utf-8") as file:
            file.write(html)
        return html

    def _download_novel_chapter(self, novel, novel_id):
        headers_generator = Headers(
            browser="chrome",
            os="win",
            headers=False
        )
        headers = headers_generator.generate()

        data = {
            "action": "nd_getchapters",
            "mypostid": novel_id,
            "mygrr": "0"
        }
        response = requests.post(url="https://www.novelupdates.com/wp-admin/admin-ajax.php",
                                 data=data,
                                 headers=headers)

        response.encoding = "utf-8"
        with open(Config.CHAPTERS_HTML_PATH + Novel.getNormalizedTitle(novel) + ".html", "w", encoding="utf-8") as file:
            file.write(response.text)
