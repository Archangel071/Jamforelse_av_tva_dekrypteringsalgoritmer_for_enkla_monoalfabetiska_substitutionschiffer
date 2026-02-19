import string

known_freq_dict = {
    'a': 0.0834,
    'b': 0.0154,
    'c': 0.0273,
    'd': 0.0414,
    'e': 0.1260,
    'f': 0.0203,
    'g': 0.0192,
    'h': 0.0611,
    'i': 0.0671,
    'j': 0.0023,
    'k': 0.0087,
    'l': 0.0424,
    'm': 0.0253,
    'n': 0.0680,
    'o': 0.0770,
    'p': 0.0166,
    'q': 0.0009,
    'r': 0.0568,
    's': 0.0611,
    't': 0.0937,
    'u': 0.0285,
    'v': 0.0106,
    'w': 0.0234,
    'x': 0.0020,
    'y': 0.0204,
    'z': 0.0006
}

def monograms(txt):
    txt_stripped = txt.replace(' ', '')

    # Count amount of ocurrances & sort them in decending order
    counts = {}
    for l in string.ascii_lowercase:
        counts.update({l:txt_stripped.count(l)})
    counts_sorted = dict(sorted(counts.items(), reverse=True, key=lambda x: x[1]))

    # Calculate the frequencies
    freqs = {}
    freqs.update(counts_sorted.copy())
    for k, v in counts.items():
        freqs.update({k : (v / len(txt_stripped))})

    # Make the guess
    lettermapping = {}
    for k, v in freqs.items():
        candidates = set()
        known_freq_dict_changeable = known_freq_dict.copy()
        index = 0
        # Use the 4 best candidates
        while index < 4:
            best_diff = 3
            for known_k, known_v in known_freq_dict_changeable.items():
                new_diff = abs(v - known_v)
                if new_diff < best_diff:
                    best_diff = new_diff
                    best_match = known_k
            candidates.add(best_match)
            known_freq_dict_changeable.pop(best_match)
            index += 1
        lettermapping.update({k : candidates})

    return lettermapping, freqs

if __name__ == '__main__':
    # Retrieve txt
    with open('../utilities/encrypted_input.txt', encoding='utf-8') as f:
        txt = f.read().lower()

    # Remove non-ascii letters
    for char in txt:
        if not char.isalpha():
            txt = txt.replace(char, '')

    guess, freqs = monograms(txt)

    guess = {}
    for k, v in freqs.items():
        best_diff = 3
        for known_k, known_v in known_freq_dict.items():
            new_diff = abs(v - known_v)
            if new_diff < best_diff:
                best_diff = new_diff
                best_match = known_k
        guess.update({k:best_match})

    #
    #
    #
    # Pick the 5 most common
    common_guesses = {k: v for i, (k, v) in enumerate(guess.items()) if i < 5}
    '''print(common_guesses)'''
    correct = 0
    for k, v in common_guesses.items():
        if ord(k) == ord(v) + 1:
            correct += 1
    '''print(correct)'''

    # Pick the 10 most common
    common_guesses = {k: v for i, (k, v) in enumerate(guess.items()) if i < 10}
    '''print(common_guesses)'''
    correct = 0
    for k, v in common_guesses.items():
        if ord(k) == ord(v) + 1:
            correct += 1
    '''print(correct)'''

    # Pick the 18 most common
    common_guesses = {k: v for i, (k, v) in enumerate(guess.items()) if i < 18}
    '''print(common_guesses)'''
    correct = 0
    for k, v in common_guesses.items():
        if ord(k) == ord(v) + 1:
            correct += 1
    '''print(correct)'''

    # Pick the 26 most common
    '''print(guess)'''
    correct = 0
    for k, v in guess.items():
        if ord(k) == ord(v) + 1:
            correct += 1
    '''print(correct)'''