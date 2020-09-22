from time import sleep

from yandex_images_download.downloader import YandexImagesDownloader, get_driver


def init_downloader(driver):
    downloader = YandexImagesDownloader(driver=driver, output_directory='./static/downloads', limit=5, pool=None)

    return downloader


def demo_task(some_args):
    print("running demo task", some_args)
    sleep(5)
    print("end demo task", some_args)
    return "OK"


if __name__ == '__main__':
    driver_ = get_driver('Firefox', path="./geckodriver")

    init_downloader(driver_).download_images(['ptn'])
    driver_.quit()
