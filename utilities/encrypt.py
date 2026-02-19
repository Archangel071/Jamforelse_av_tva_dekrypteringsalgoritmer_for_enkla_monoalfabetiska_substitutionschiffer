import string

with open('../sample_texts/gibberish.txt', encoding='utf-8') as plaintext:
    plaintext = plaintext.read().lower()

translation_table = str.maketrans(string.ascii_lowercase, "bcdefghijklmnopqrstuvwxyza")

encrypted_text = plaintext.translate(translation_table)
with open('encrypted_input.txt', 'w', encoding='utf-8') as f:
    f.write(encrypted_text)

print(plaintext)
print(encrypted_text)