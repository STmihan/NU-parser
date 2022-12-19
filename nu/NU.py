import json as JSON
import random
from pathlib import Path
from time import sleep

from tqdm import tqdm

import Config
import nu.NovelUpdatesDownloader as Downloader
import nu.NovelUpdatesParser as Parser
import nu.NovelUpdatesSaver as Saver
import nu.types


def _validate_url(url):
    pg_ = "&pg="
    if url.endswith(pg_):
        return url
    if not url.startswith("https://www.novelupdates.com/series-finder/"):
        raise Exception("Invalid URL")
    if url.endswith("&") or url.endswith("?") or url.endswith("="):
        raise Exception("Invalid URL")

    find = url.find(pg_)
    if find == -1:
        url += pg_
    i = find + 4
    page = url[i]
    url = url.replace(pg_ + page, "")
    print("URL: " + url)
    url += pg_
    return url


class NU:
    downloader: Downloader.NovelUpdatesDownloader
    parser: Parser.NovelUpdatesParser
    saver: Saver.NovelUpdatesJsonSave

    def __init__(self):
        with open("data/link.txt", "w") as f:
            f.write(f'URL: {Config.URL}')
        Config.URL = _validate_url(Config.URL)
        self.downloader = Downloader.NovelUpdatesDownloader()
        self.parser = Parser.NovelUpdatesParser()
        self.saver = Saver.NovelUpdatesJsonSave()

    def get_page_count(self):
        html = self.downloader.get_search_html(1)
        return self.parser.get_page_count(html)

    def update_html_data(self):
        page_count = self.get_page_count()

        print("Updating search data...")
        r = tqdm(range(1, page_count + 1),
                 desc="Pages",
                 leave=True,
                 colour="white")
        for i in r:
            r.set_description(f"Updating page {i}")
            self.downloader.get_search_html(i, force=True)

    def get_search_page(self, page_number):
        html = self.downloader.get_search_html(page_number)
        return self.parser.parse_search_page(html)

    def get_all_novels(self):
        results = []
        path = Config.SEARCH_JSON_PATH + Config.SEARCH_JSON_FILE_NAME
        if not Path(path).exists():
            self.update_html_data()
        with open(path, "r", encoding="utf-8") as file:
            json = JSON.loads(file.read())
            for item in tqdm(json, desc="Searching", leave=True, colour="white"):
                results.append(nu.Novel.fromDict(item))

        return results

    def get_novel_html(self, title):
        html = self.downloader.get_novel_html(title)
        return html

    def get_novel_chapters(self, novel):
        novel_id = self.get_novel_id(novel)
        html = self.downloader.get_novel_chapter_html(novel, novel_id)
        return self.parser.parse_novel_chapters_page(html, novel, novel_id)

    def get_novel_id(self, novel):
        html = self.downloader.get_novel_html(novel)
        page = self.parser.parse_novel_page(novel, html)
        return page.novelId
