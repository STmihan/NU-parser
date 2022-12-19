from bs4 import BeautifulSoup

from nu.types import Novel, NovelFull, ChaptersList


def _get_related_novels(soup):
    relatedTitle = {}
    seriesOtherList = soup.find_all('h5', {'class': 'seriesother'})
    for other in seriesOtherList:
        if other.text == 'Related Series':
            relatedTitle = other
            break
    related = []
    while relatedTitle.find_next().text != "Recommendations":
        relatedTitle = relatedTitle.find_next()
        if relatedTitle.name == 'a':
            related_novel_id = relatedTitle.get('id').replace('sid', '')
            related.append({'title': relatedTitle.text,
                            'novel_id': related_novel_id,
                            'type': relatedTitle.next_sibling.text.strip().replace('(', '').replace(')', ''),
                            'url': 'https://www.novelupdates.com/?p=' + related_novel_id})

    return related


def _parse_chapter_span(span):
    return {"label": span.text, "link": span.parent.get('href').replace("//", "https://")}


class NovelUpdatesParser:

    def parse_search_page(self, html):
        soup = BeautifulSoup(html, "lxml")
        finds = soup.find_all(class_="search_main_box_nu")
        result = []
        for find in finds:
            result.append(self.parse_search_block(find))

        return result

    def parse_search_block(self, block):
        title = block.find(class_="search_title").find('a').text
        chapters_count = block.find("i", {"title": "Chapter Count"}).find_parent().text.split()[0]
        rating = block.find(class_="search_ratings").text.split().pop().replace('(', '').replace(')', '')
        genre = list(map(lambda tag: tag.text, block.find(class_="search_genre").find_all("a")))
        link = block.find(class_="search_title").find('a').get('href')

        search_block = block.find(class_="search_body_nu").contents
        description = "" if len(search_block) < 4 else search_block[3].text
        testhide = block.find("span", {"class": "testhide"})
        if testhide is not None:
            description += testhide.text
        description = description[:description.rfind('\n')]  # remove last line

        novel = Novel(title, chapters_count, rating, genre, description, link)

        return novel.__dict__

    def get_page_count(self, html):
        soup = BeautifulSoup(html, "lxml")
        return int(soup.find(class_="digg_pagination").find_all("a")[-2].text)

    def parse_novel_page(self, novel, html, pretty=False):
        soup = BeautifulSoup(html, "lxml")
        novel_id = soup.find('link', {'rel': 'shortlink'}).get('href').split('/')[-1].replace('?p=', '')
        description = soup.find('div', {'id': 'editdescription'}).text.strip()
        tags = list(map(lambda tag: tag.text, soup.find('div', {'id': 'showtags'}).find_all('a')))
        show_type_block = soup.find('div', {'id': 'showtype'})
        type = show_type_block.find('a').text.strip() if show_type_block.find('a') is not None else ""
        names = list(
            filter(None, list(map(lambda tag: tag.text.strip(), soup.find('div', {'id': 'editassociated'}).contents))))
        authors = list(map(lambda tag: tag.text, soup.find('div', {'id': 'showauthors'}).find_all('a')))
        year = soup.find('div', {'id': 'edityear'}).text.strip()
        language = soup.find('div', {'id': 'showlang'}).find('a').text.strip()
        related = _get_related_novels(soup)

        novelFull = NovelFull(novel_id, novel.title, description, novel.link, novel.rating, novel.chapters_count,
                              novel.genre, tags, type, names, authors, year, language, related)

        return novelFull

    def parse_novel_chapters_page(self, html, novel, novel_id):
        soup = BeautifulSoup(html, "lxml")
        find_all = soup.find_all('span')
        find_all.pop(0)
        chapters = list(map(_parse_chapter_span, find_all))
        chapters.reverse()

        return ChaptersList(novel_id, novel.title, chapters)
