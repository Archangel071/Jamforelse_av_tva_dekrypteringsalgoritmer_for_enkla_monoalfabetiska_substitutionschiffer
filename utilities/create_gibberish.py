import string
import random

txt = ''
letters = string.ascii_lowercase + 6 * ' '
words = 0
c_prev = ''

while words < 3000:
    c = random.choice(letters)
    if c_prev == c:
        continue
    txt += c
    if c == ' ':
        words += 1
    c_prev = c

with open('../sample_texts/gibberish.txt', 'w', encoding='utf-8') as f:
    f.write(txt)