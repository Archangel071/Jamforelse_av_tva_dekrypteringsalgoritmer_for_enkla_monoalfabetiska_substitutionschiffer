with open('../dictionaries/combined_dictionaries.txt', encoding='utf-8') as f:
    words = f.readlines()
    for i, word in enumerate(words):
        words[i] = word.replace('\n', '')

all_words_map = {}
for word in words:
    index = 0
    mapping_dict = {}
    mapping_list = []
    for char in word:
        if char not in mapping_dict:
            mapping_dict[char] = index
            index += 1
        mapping_list.append(mapping_dict[char])
    mapping_list = tuple(mapping_list)
    if mapping_list not in all_words_map:
        possible_words = {word}
    else:
        possible_words = all_words_map[mapping_list]
        possible_words.add(word)
    all_words_map.update({mapping_list: possible_words})

with open('all_wordmaps.py', 'w', encoding='utf-8') as f:
    f.write('all_wordmaps = ' + str(all_words_map))