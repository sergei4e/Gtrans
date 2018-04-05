============
gtrans
============

Free Google Translate API. It works with selenium and Chrome.
For each translation it uses public Google Translate web service.

Requerements:
-------------

* Python 3.6
* [Google Chrome](https://www.google.com/chrome/)
* [selenium](http://selenium-python.readthedocs.io/installation.html)
* [lxml](http://lxml.de/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [nltk](https://www.nltk.org/)

Features
--------
* Text translation
* HTML markuped text translation


Installation
------------
::

  $ pip install gtrans

Example usage
-------------
.. code-block:: python

    from gtrans import translate_text, translate_html

    text = '''
    Jones and Palin met at Oxford University, where they performed together 
    with the Oxford Revue. Chapman and Cleese met at Cambridge University. 
    Idle was also at Cambridge, but started a year after Chapman and Cleese.
    '''

    html = '''
    <h1>Нил Армстронг</h1>
    <p>Нил Армстронг родился в городе Уапаконета, штат Огайо,
    в семье Стивена Армстронга и Виолы Энгель.</p>
    <p>Родился 5 августа 1930 года. Он имел шотландско-ирландское
    и немецкое происхождение.</p>
    <p>У него были младшие сестра и брат: Джун и Дин. Отец,
    Стивен Армстронг, работал
    аудитором на правительство штата, и после рождения Нила
    семья часто переезжала из
    города в город: они успели пожить в двадцати различных
    городах до того, как окончательно
    осели в Уапаконете (штат Огайо) в 1944 году.</p>
    '''

    print('*'*50)
    print(translate_text(text, 'en', 'ru'))
    print('='*50)
    print(translate_html(html, 'ru', 'en'))
    print('*'*50)

Output
------
.. code-block::

    **************************************************
    Джонс и Пэйлин встретились в Оксфордском университете, где они выступали вместе с Oxford Revue. 
    Чепмен и Клиз встретились в Кембриджском университете. Идл был также в Кембридже, но начал через 
    год после Чепмена и Клиса.
    ==================================================
    <h1>Neil Armstrong</h1> <p>Neil Armstrong was born in Huapakoneta, Ohio, to the family 
    of Stephen Armstrong and Viola Engel.</p> <p>He was born on August 5, 1930. He had Scottish-Irish 
    and German descent.</p> <p>He had a younger sister and brother: June and Dean. Father Steven Armstrong 
    worked as an auditor for the state government, and after the birth of Neil, the family often moved 
    from city to city: they managed to live in twenty different cities before finally settling in Wapakonet, 
    Ohio, in 1944.</p>
    **************************************************

Changelog
---------

0.2
~~~

* updates in modules
* multithreading mode
* updates in markuped text translation
* change PhantomJS to Chromedriver

0.1
~~~~~

* First published working version.

Author
------

Sergii Chernenko <mailto:4e.sergei@gmail.com>
