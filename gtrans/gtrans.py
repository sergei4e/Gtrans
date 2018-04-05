import re
import gc
from time import sleep
from lxml import html
from collections import OrderedDict
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from nltk import sent_tokenize
from .browser import get_chrome


def worker(q, lf, lt, result):
    brows = None
    while q.qsize():
        try:
            part = q.get()
            if not brows:
                brows = get_chrome()
            if part.startswith('http') and '//' in part and len(part.strip().split()) == 1:
                result[part] = part
                continue
            url = f'http://translate.google.com/#{lf}/{lt}/'
            brows.get(url)
            sleep(0.5)
            corpart = part.replace("'", "\\'")
            brows.execute_script(f"document.getElementById('source').value = '{corpart}'; ")
            textarea = brows.find_element_by_id('source')
            textarea.click()
            mobile = True
            bottons = ['//*[@id="gt-submit"]', '//div[@class="go-wrap"]']
            for b in bottons:
                try:
                    brows.find_element_by_xpath(b).click()
                    if b == '//*[@id="gt-submit"]':
                        mobile = False
                    continue
                except Exception:
                    pass
            tr_part, c = '', 0
            while not tr_part and c < 10:
                sleep(0.5)
                if mobile:
                    elements = html.fromstring(brows.page_source).xpath(
                        "//span[contains(@class, 'tlid-translation')]")
                    temp = ' '.join([html.tostring(t).decode('utf-8') for t in elements])
                    tr_part = BeautifulSoup(temp, 'html.parser').get_text()
                else:
                    elements = html.fromstring(brows.page_source).xpath(
                        '//span[@id="result_box"]')
                    temp = ' '.join([html.tostring(t).decode('utf-8') for t in elements])
                    tr_part = BeautifulSoup(temp, 'html.parser').get_text()
                if tr_part == 'Translating...':
                    tr_part = ''
                c += 1
            result[part] = re.sub(r"(&.{2,8}?;)", " ", tr_part)
        except Exception as e:
            print(type(e), e)
            result[part] = ''
    if brows:
        brows.stop_client()
        brows.close()
        brows.quit()
        del (brows)


def translate_text(text, lf, lt):
    text = ' '.join(text.split())
    parts = Queue()
    if len(text) <= 4000:
        parts.put(text)
    else:
        sents = sent_tokenize(text)
        part = ''
        for sent in sents:
            part = sent + ' '
            if len(part) > 4000:
                parts.put(part.strip())
                part = ''
        else:
            parts.put(part.strip())
    result = OrderedDict()
    max_workers = 2
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(max_workers):
            executor.submit(worker, parts, lf, lt, result)
    translated_text = ' '.join([x for x in result.values()])
    gc.collect()
    return translated_text


def translate_html_slow(code, lf, lt):
    code = ' '.join(code.split())
    regular = re.compile(r"(?<=[>]).*?(?=[<])", re.S)
    text_parts = regular.findall(code)
    text_parts = [x.strip() for x in text_parts if len(x.strip()) > 3]
    qparts = Queue()
    for p in text_parts:
        qparts.put(p)
    result = OrderedDict()
    max_workers = 2
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(max_workers):
            executor.submit(worker, qparts, lf, lt, result)
    for part in result:
        code = code.replace(part, result[part], 1)
    gc.collect()
    return code


def translate_html(code, lf, lt):
    code = ' '.join(code.split())
    regular = re.compile(r"(?<=[>]).*?(?=[<])", re.S)
    text_parts = regular.findall(code)
    text_parts = [x.strip() for x in text_parts if len(x.strip()) > 3]
    text = ' +++ '.join(text_parts)

    parts = Queue()
    if len(text) <= 4000:
        parts.put(text)
    else:
        sents = sent_tokenize(text)
        part = ''
        for sent in sents:
            part += sent + ' '
            if len(part) > 4000:
                parts.put(part.strip())
                part = ''
        else:
            parts.put(part.strip())

    result = OrderedDict()
    pre_result = OrderedDict()

    max_workers = 2
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(max_workers):
            executor.submit(worker, parts, lf, lt, pre_result)

    q2 = Queue()

    for textpart, tr_textpart in pre_result.items():
        tp = [x.strip() for x in textpart.split('+++')]
        ttp = [x.strip() for x in tr_textpart.replace('+ +', '++').split('+++')]

        if len(tp) == len(ttp):
            for i in range(len(tp)):
                result[tp[i]] = ttp[i]
        else:
            for p in tp:
                q2.put(p)

    if q2.qsize():
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for _ in range(max_workers):
                executor.submit(worker, q2, lf, lt, result)

    for part in result:
        code = code.replace(part, result[part], 1)

    gc.collect()

    return code


if __name__ == '__main__':
    print(translate_text('hello world', 'en', 'ru'))
