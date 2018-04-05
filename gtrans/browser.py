import os
import random
from selenium import webdriver

_uafile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uagents.txt')
with open(_uafile) as f:
    uagents = [ua.strip() for ua in f if ua.strip()]


def get_chrome(proxy=None, useragent='random'):
    _driver = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver')
    _options = webdriver.chrome.options.Options()
    _options.add_argument("--headless")
    _options.add_argument("--no-sandbox")
    _options.add_argument("--disable-notifications")
    if useragent == 'random':
        _options.add_argument(f"user-agent={random.choice(uagents)}")
    elif useragent == 'custom':
        pass
    else:
        _options.add_argument(f"user-agent={useragent}")
    if proxy:
        _options.add_argument('--proxy-server=socks5://{}'.format(proxy))
    browser = webdriver.Chrome(options=_options, executable_path=_driver)
    browser.set_page_load_timeout(60)
    browser.set_window_size(1366, 768)
    return browser


def get_with_chrome(url, proxy=None, useragent='random'):
    browser = get_chrome(proxy, useragent)
    try:
        browser.get(url)
        code = browser.page_source
    except:
        code = ''
    finally:
        browser.stop_client()
        browser.close()
        browser.quit()
        del (browser)
    return code


if __name__ == '__main__':
    code = get_with_chrome('http://proxyjudge.us/azenv.php')
    print(code)
