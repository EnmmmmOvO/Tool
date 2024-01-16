import getpass
import os.path
import platform
import requests
import warnings
import selenium.common
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class MyError(Exception):
    pass


def url_explanation(url):
    warnings.filterwarnings('ignore')
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except selenium.common.exceptions.WebDriverException:
        try:
            driver = webdriver.Edge(service=EdgeService(executable_path=EdgeChromiumDriverManager().install()))
        except selenium.common.exceptions.WebDriverException:
            print('Google Chromium or Edge cannot open')
            exit(1)

    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(EC.url_changes(url))
        if not EC.url_to_be('https://au.bbcollab.com/collab/ui/session/playback'):
            raise Exception('Download failure: Bb collaborate URL is invalid, Obtain it again!')
        video_url = BeautifulSoup(driver.page_source, 'html.parser').find_all('video')[0].get('src')
        if video_url is None: raise Exception('Download failure: Failed to resolve the URL address of the video!')
        driver.quit()
    except MyError:
        driver.quit()
        print(MyError)
        exit(1)
    except selenium.common.TimeoutException:
        driver.quit()
        print('Download failure: Connection timeout or Wrong Bb collaborate URL!')
        exit(1)
    except IndexError:
        driver.quit()
        print('Download failure: Failed to resolve the URL address of the video!')
        exit(1)

    return video_url


def video_download(video_url):
    path = str()

    if platform.system() == 'Windows':
        path = 'C:/Users/' + getpass.getuser() + '/Downloads/'
    elif platform.system() == 'Darwin':
        path = '/Users/' + getpass.getuser() + '/Downloads/'

    if not os.path.exists(path):
        path = os.getcwd() + '/Downloads/'
        if not os.path.exists(path):
            os.mkdir(path)

    temp_list = video_url.split('.mp4')[0].split('/')
    path += temp_list[len(temp_list) - 1]

    if os.path.exists(path + '.mp4'):
        temp = 0
        while os.path.exists(path + '_' + str(temp) + '.mp4'):
            temp += 1
        path += '_' + str(temp) + '.mp4'
    else:
        path += '.mp4'

    r = requests.get(video_url, stream=True)
    content_size = int(int(r.headers['content-length']) / 1024 / 1024)

    print('\nStart Download ' + path)
    try:
        with open(path, 'wb') as f:
            for data in tqdm(iterable=r.iter_content(1024 * 1024), total=content_size, unit='MB', dynamic_ncols=True,
                             desc='Download Process'):
                f.write(data)
        print('Download completed!')
    except Exception:
        print('Download failure: Cannot download the file!')
        exit(1)


if __name__ == '__main__':
    web_url = str()
    try:
        web_url = input('Enter the Bb collaborate URL: ')
    except KeyboardInterrupt:
        exit(1)
    video_url = url_explanation(web_url)
    video_download(video_url)
