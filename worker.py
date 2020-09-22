import spacy
from rq import Worker as Base
from yandex_images_download.downloader import YandexImagesDownloader, get_driver


downloader: YandexImagesDownloader = None
driver = None
nlp = None


class Worker(Base):
    def __init__(self, queues=None, *args, **kwargs):
        super().__init__(queues, *args, **kwargs)
        global downloader, driver, nlp
        nlp = spacy.load('ru2')
        driver = get_driver('Firefox', path="./geckodriver")
        downloader = YandexImagesDownloader(driver=driver, output_directory='./static/downloads',
                                            limit=4, exact_isize=[1080, 1920])

    def request_stop(self, *args, **kwargs):
        global driver
        driver.quit()
        super().request_stop(*args, **kwargs)


def clean_text(text):
    global nlp
    pos_tags = ['NOUN', 'PROPN', 'ADJ']
    cleaned = []
    for token in nlp(text):
        if token.pos_ in pos_tags and not token.is_stop:
            cleaned.append(token.text)
    if len(cleaned) > 0:
        return cleaned
    else:
        return None


def download_images_task(text):
    global downloader
    keywords = clean_text(text)
    if keywords is not None:
        results = downloader.download_images([" ".join(keywords)])
    files = []
    for image in results.keyword_results:
        if len(image.keyword) > 0:
            for page in image.page_results:
                files.extend([r.img_path for r in page.img_url_results])
    return text, keywords, files
