from munch import Munch

from utils.name_normilizer import normalize_name
import json as JSON


class Novel:
    title = ""
    chapters_count = 0
    rating = 0
    genre = []
    description = ""
    link = ""

    def __init__(self, title, chapters_count, rating, tags, description, link):
        self.title = title
        self.chapters_count = chapters_count
        self.rating = rating
        self.genre = tags
        self.description = description
        self.link = link

    @staticmethod
    def getNormalizedTitle(self):
        return normalize_name(self.title)

    def __str__(self):
        return JSON.dumps(self.__dict__, ensure_ascii=False)

    @staticmethod
    def fromDict(d):
        return Munch.fromDict(d)


class NovelFull:
    novelId = 0

    title = ""
    description = ""
    link = ""
    rating = 0
    chapters_count = 0
    genre = []
    tags = []
    type = ""

    names = []
    authors = []

    year = ""
    language = ""

    related = []

    def __init__(self, novel_id, title, description, link, rating, chapters_count, genre, tags, type, names, authors,
                 year, language, related):
        self.novelId = novel_id
        self.title = title
        self.description = description
        self.link = link
        self.rating = rating
        self.chapters_count = chapters_count
        self.genre = genre
        self.tags = tags
        self.type = type
        self.names = names
        self.authors = authors
        self.year = year
        self.language = language
        self.related = related

    def __str__(self):
        return JSON.dumps(self.__dict__, ensure_ascii=False)

    @staticmethod
    def getNormalizedTitle(self):
        return normalize_name(self.title)

    @staticmethod
    def fromDict(d):
        return Munch.fromDict(d)


class ChaptersList:
    novelId = 0
    title = ""
    chapters = []

    def __init__(self, novel_id, title, chapters):
        self.novelId = novel_id
        self.title = title
        self.chapters = chapters

    def __str__(self):
        return JSON.dumps(self.__dict__, ensure_ascii=False)

    @staticmethod
    def fromDict(d):
        return Munch.fromDict(d)
