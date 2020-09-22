from rq import Worker as Base
from yandex_images_download.downloader import YandexImagesDownloader, get_driver


downloader: YandexImagesDownloader = None
driver = None


class Worker(Base):
    def __init__(self, queues=None, *args, **kwargs):
        super().__init__(queues, *args, **kwargs)
        global downloader, driver
        driver = get_driver('Firefox', path="./geckodriver")
        downloader = YandexImagesDownloader(driver=driver, output_directory='./static/downloads', limit=5, pool=None)

    def request_stop(self, *args, **kwargs):
        global driver
        driver.quit()
        super().request_stop(*args, **kwargs)


def download_images_task(text):
    global downloader
    downloader.download_images([text])
    return True
