from pathlib import Path

import Config
from nu.types import Novel, NovelFull
import json as JSON


def _save_json(data, path, pretty):
    with open(path, "w", encoding="utf-8") as f:
        json = JSON.dumps(data,
                          default=lambda o: o.__dict__,
                          ensure_ascii=False,
                          indent=4 if pretty else None)
        f.write(json)


class NovelUpdatesJsonSave:
    def __init__(self):
        Path(Config.SEARCH_JSON_PATH).mkdir(parents=True, exist_ok=True)
        Path(Config.NOVELS_JSON_PATH).mkdir(parents=True, exist_ok=True)
        Path(Config.CHAPTERS_JSON_PATH).mkdir(parents=True, exist_ok=True)

    def save_search(self, data, pretty=False):
        novels = []
        for novel in data:
            novels.append(Novel.fromDict(novel))

        json_path = Config.SEARCH_JSON_PATH + Config.SEARCH_JSON_FILE_NAME
        _save_json(novels, json_path, pretty)

    def save_novel(self, novel_full, pretty):
        json_path = Config.NOVELS_JSON_PATH + NovelFull.getNormalizedTitle(novel_full) + ".json"
        _save_json(novel_full, json_path, pretty)

    def save_chapters_list(self, chapters, novel, pretty=False):
        json_path = Config.CHAPTERS_JSON_PATH + Novel.getNormalizedTitle(novel) + ".json"
        _save_json(chapters, json_path, pretty)
