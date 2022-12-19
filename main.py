from datetime import datetime

import tqdm

import nu as NovelUpdates
from nu import Novel


def save_search(update=False, pretty=False):
    nu = NovelUpdates.NU()
    page_count = nu.get_page_count()
    print("Found " + str(page_count) + " pages.")
    if update:
        nu.update_html_data()
    results = []
    print("Saving search data...")
    t = tqdm.tqdm(range(1, page_count + 1), desc="Pages", leave=True, colour="white")
    for i in t:
        t.set_description(f"Saving page {i}")
        results += nu.get_search_page(i)

    nu.saver.save_search(results, pretty)


def save_novels(update=False, pretty=False):
    nu = NovelUpdates.NU()
    print("Searching for novels...")
    if update:
        print("Updating novel data...")
        save_search(update=True, pretty=pretty)

    print("Loading search data...")
    novels = nu.get_all_novels()
    print("Found " + str(len(novels)) + " novels.")
    print("Saving novels...")
    t = tqdm.tqdm(novels, desc="Novels", leave=True, colour="white")
    for i in t:
        novel = Novel.fromDict(i)
        html = nu.downloader.get_novel_html(novel)
        novelFull = nu.parser.parse_novel_page(novel, html, pretty)
        nu.saver.save_novel(novelFull, pretty)


def save_chapters_list(pretty=False):
    nu = NovelUpdates.NU()
    print("Getting novel list...")
    novels = nu.get_all_novels()
    print("Searching for chapters...")
    t = tqdm.tqdm(novels, desc="Chapters", leave=True, colour="white")
    for novel in t:
        novel = Novel.fromDict(novel)
        chapters = nu.get_novel_chapters(novel)
        t.set_description(f"Searching for {len(chapters.chapters)} chapters")
        nu.saver.save_chapters_list(chapters=chapters, novel=novel, pretty=pretty)


def save_all(pretty=False):
    save_search(pretty=pretty)
    save_novels(pretty=pretty)
    save_chapters_list(pretty=pretty)


def main():
    time = datetime.now()
    save_all(True)
    print("Done in " + str(datetime.now() - time))


if __name__ == "__main__":
    main()
