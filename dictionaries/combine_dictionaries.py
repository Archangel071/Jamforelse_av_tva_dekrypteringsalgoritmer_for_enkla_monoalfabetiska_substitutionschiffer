with open('../dictionaries/MIT_words.txt', encoding='utf-8') as f:
    mit_words = f.read().lower().split('\n')

with (open('../dictionaries/Sweigart_words.txt', encoding='utf-8') as f):
    sweigart_words = f.read().lower().split('\n')

print(mit_words)
print(sweigart_words)
seen = set()
combined_words = [x for x in mit_words + sweigart_words if x not in seen and not seen.add(x)]

print(seen)
print(len(mit_words), len(sweigart_words), len(combined_words))

with open('combined_dictionaries.txt', 'w', encoding='utf-8') as f:
    for word in combined_words:
        f.write(word + '\n')