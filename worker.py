from rq import Worker as Base
from yandex_images_download.downloader import YandexImagesDownloader, get_driver


downloader: YandexImagesDownloader = None
driver = None


class Worker(Base):
    def __init__(self, queues=None, *args, **kwargs):
        super().__init__(queues, *args, **kwargs)
        global downloader, driver
        driver = get_driver('Firefox', path="./geckodriver")
        downloader = YandexImagesDownloader(driver=driver, output_directory='./static/downloads',
                                            limit=3, exact_isize=[1080, 1920])

    def request_stop(self, *args, **kwargs):
        global driver
        driver.quit()
        super().request_stop(*args, **kwargs)


def download_images_task(text):
    global downloader
    results = downloader.download_images([text])
    files = []
    for image in results.keyword_results:
        if image.keyword == text:
            for page in image.page_results:
                files.extend([r.img_path for r in page.img_url_results])
    return text, files

