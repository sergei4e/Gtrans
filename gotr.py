# coding: utf-8
import time
import re
from selenium import webdriver
from lxml import html
from bs4 import BeautifulSoup


class GoogleTranslate(object):

    BASE = 'https://translate.google.com/'
    XPATH = '//span[@id="result_box"]/span/text()'

    # https://translate.google.com.ua/#en/ru/hello world

    @staticmethod
    def text_into_queries(text):
        text = text.replace('\n', ' $$ ').replace('%', '()')
        if len(text) <= 8000:
            return [text]
        else:
            words = text.split(' ')
            part, queries = '', []
            for word in words:
                if len(part) <= 8000:
                    part += word + ' '
                else:
                    part = " ".join(part.split()).strip()
                    queries.append(part)
                    part = word + ' '
            else:
                part = " ".join(part.split()).strip()
                queries.append(part)
            return queries

    @staticmethod
    def get_text(page):
        tree = html.fromstring(page)
        return ' '.join(tree.xpath(GoogleTranslate.XPATH))

    @staticmethod
    def clean_text(text):
        text = text.replace('  ', ' ').replace(' .', '.').replace(' "', '"').replace(" '", "'")
        text = text.replace(' ,', ',').replace(' ?', '?').replace(' !', '!').replace('..', '.')
        return text.replace('$ $', '$$').replace('$$', '\n').replace('()', '%').replace('( )', '%')

    @staticmethod
    def get_text_from_code(code):
        regular = re.compile(r"(?<=[>]).*?(?=[<])", re.S)
        text_path = regular.findall(code)
        text_with_pluses = ' ___ '.join(text_path)
        return text_with_pluses

    @staticmethod
    def create_code_with_text(code, text):
        regular = re.compile(r"(?<=[>]).*?(?=[<])", re.S)
        text_path = regular.findall(code)
        new_text_path = text.split('___')
        for i, j in enumerate(text_path):
            code = code.replace(j, new_text_path[i], 1)
        return code

    @staticmethod
    def cleaner(code):
        spec_symb = ['&nbsp;', '&shy;', '&para;', '&nbsp', '&shy', '&para']
        for item in spec_symb:
            code = code.replace(item, ' ')
        return code.replace(' .', '.').replace(' ,', ',')

    @staticmethod
    def translate_text(text, from_lang='ru', to_lang='uk'):
        translated = []
        for part in GoogleTranslate.text_into_queries(text):
            url = GoogleTranslate.BASE + '#' + from_lang + '/' + to_lang + '/' + part
            driver = webdriver.Firefox()
            driver.get(url)
            time.sleep(3)
            source = driver.page_source.encode('utf-8')
            driver.quit()
            translated_part = GoogleTranslate.clean_text(GoogleTranslate.get_text(source))
            translated.append(translated_part)
        translated_text = ' '.join(translated)
        return GoogleTranslate.clean_text(translated_text)

    @staticmethod
    def translate_code(code, from_lang='ru', to_lang='uk'):
        soup = BeautifulSoup(code, 'html.parser')
        code = GoogleTranslate.cleaner(soup.prettify())
        prepared = GoogleTranslate.get_text_from_code(code)
        from_google = GoogleTranslate.translate_text(prepared, from_lang, to_lang)
        text = GoogleTranslate.clean_text(from_google)
        return GoogleTranslate.create_code_with_text(code, text)

    @staticmethod
    def translate_list(li, from_lang='ru', to_lang='uk'):
        prepared = ' . '.join(li)
        from_google = GoogleTranslate.translate_text(prepared, from_lang, to_lang)
        text = GoogleTranslate.clean_text(from_google)
        new = text.split('.')
        if len(li) != len(new) and '' not in new and ' ' not in new:
            raise ValueError('bad translation, empty elements', len(li), len(new))
        return [x.strip() for x in new]

    @staticmethod
    def examples():

        t = """
        Пропа́н, C3H8 — органическое вещество класса алканов. Содержится в природном газе,
        образуется при крекинге нефтепродуктов, при разделении попутного нефтяного газа, «жирного»
        природного газа, как побочная продукция при различных химических реакциях. Чистый пропан не
        имеет запаха, однако в технический газ могут добавляться компоненты, обладающие запахом. Как
        представитель углеводородных газов пожаро- и взрывоопасен. Малотоксичен, но оказывает вредное
        воздействие на центральную нервную систему (обладает слабыми наркотическими свойствами)[1][2].
        """

        h = """
        <ul>
        <li>При кровельных работах.</li>
        <li>При дорожных работах для разогрева битума и асфальта.</li>
        <li>В качестве топлива для переносных электрогенераторов.</li>
        <li>Для обогрева производственных помещений в строительстве.</li>
        <li>Для обогрева производственных помещений (на фермах, птицефабриках, в теплицах).</li>
        <li>Для газовых плит, водогрейных колонок в пищевой промышленности.</li>
        </ul>
        """

        l = ['производственных', 'помещений', 'в строительстве']

        print gt.translate_text(t, 'ru', 'uk')
        print gt.translate_code(h, 'ru', 'uk')
        print gt.translate_list(l, 'ru', 'uk')


if __name__ == '__main__':
    gt = GoogleTranslate()
    gt.examples()
