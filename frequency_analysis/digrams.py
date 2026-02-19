import string

known_freq_dict = {
    'th': 0.0399,
    'he': 0.0365,
    'an': 0.0217,
    'er': 0.0211,
    'in': 0.0210,
    're': 0.0164,
    'nd': 0.0162,
    'ou': 0.0141,
    'en': 0.0137,
    'on': 0.0136,
    'ed': 0.0129,
    'to': 0.0124,
    'it': 0.0124,
    'at': 0.0117,
    'ha': 0.0117,
    've': 0.0111,
    'as': 0.0109,
    'or': 0.0109,
    'hi': 0.0107,
    'ar': 0.0106,
    'te': 0.0100,
    'es': 0.0100,
    'ng': 0.0099,
    'is': 0.0099,
    'st': 0.0096,
    'le': 0.0095,
    'al': 0.0093,
    'ti': 0.0092,
    'se': 0.0085,
    'ea': 0.0084,
    'wa': 0.0084,
    'me': 0.0083,
    'nt': 0.0077,
    'ne': 0.0075,
}

def get_empty_lettermapping():
    return {'a': set(), 'b': set(), 'c': set(), 'd': set(), 'e': set(),
            'f': set(), 'g': set(), 'h': set(), 'i': set(), 'j': set(),
            'k': set(), 'l': set(), 'm': set(), 'n': set(), 'o': set(),
            'p': set(), 'q': set(), 'r': set(), 's': set(), 't': set(),
            'u': set(), 'v': set(), 'w': set(), 'x': set(), 'y': set(),
            'z': set()}

def add_lettermapping_to_intersect(mapA, mapB):
    intersectedMapping = get_empty_lettermapping()
    for letter in string.ascii_lowercase:

        # An empty set means "any letter is possible". In this case just
        # copy the other map entirely:
        if len(mapA[letter]) == 0:
            intersectedMapping[letter] = mapB[letter]
        elif len(mapB[letter]) == 0:
            intersectedMapping[letter] = mapA[letter]
        else:
            # If a letter exists in both mapA[letter] and mapB[letter],
            # add that letter to intersectedMapping[letter]:
            intersectedMapping[letter] = mapA[letter].intersection(mapB[letter])

    return intersectedMapping

def digrams(txt):
    # Extract all digrams from the text, excluding those which includes a space
    # Then add them to a dictionary and increment oucurrances
    all_digrams_txt = ()
    digrams_txt = {}
    for i, char in enumerate(txt):
        if i == len(txt) - 1:
            continue
        if char == ' ' or txt[i+1] == ' ':
            continue
        digram = char + txt[i + 1]
        all_digrams_txt += (digram,)
        try:
            digrams_txt[digram] += 1
        except KeyError:
            digrams_txt.update({digram: 1})

    # Sort the digrams in decending order
    sorted_digrams = sorted(digrams_txt.items(), key=lambda x: x[1], reverse=True)

    # Pick out the 34 most common since the data only contains the 34 most common
    sorted_common_digrams = {}
    for i, (k, v) in enumerate(sorted_digrams):
        if i >= 34:
            break
        sorted_common_digrams.update({k: v})

    # Calculate the frequencies
    digrams_freqs = {k: v/len(all_digrams_txt) for k, v in sorted_common_digrams.items()}

    # Create the initial guess of which digrams could be which
    digrammapping = {}
    for k, v in digrams_freqs.items():
        candidates = ()
        known_freq_dict_changeable = known_freq_dict.copy()
        ind = 0
        # Use the 4 best matches
        while ind < 4:
            best_diff = 3
            for known_k, known_v in known_freq_dict_changeable.items():
                new_diff = abs(v - known_v)
                if new_diff < best_diff:
                    best_diff = new_diff
                    best_match = known_k
            candidates += (best_match,)
            known_freq_dict_changeable.pop(best_match)
            ind += 1
        digrammapping.update({k: candidates})

    # Create a "regular" lettermapping from the digram mapping
    intersect = get_empty_lettermapping()
    lettermapping = get_empty_lettermapping()
    for k, v in digrammapping.items():
        for digram in v:
            lettermapping[k[0]].add(digram[0],)
            lettermapping[k[1]].add(digram[1],)

        intersect = add_lettermapping_to_intersect(intersect, lettermapping)

    return intersect

if __name__ == '__main__':
    # Retrieve txt
    with open('../utilities/encrypted_input.txt', encoding='utf-8') as f:
        txt = f.read().lower()

    # Remove non-ascii letters
    for char in txt:
        if not char.isalpha():
            txt = txt.replace(char, '')

    digrams(txt)