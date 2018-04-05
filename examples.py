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
