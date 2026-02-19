from wordmaps.all_wordmaps import *
import string
import time

start = time.time()

def get_empty_lettermapping():
    return {'a': set(), 'b': set(), 'c': set(), 'd': set(), 'e': set(),
            'f': set(), 'g': set(), 'h': set(), 'i': set(), 'j': set(),
            'k': set(), 'l': set(), 'm': set(), 'n': set(), 'o': set(),
            'p': set(), 'q': set(), 'r': set(), 's': set(), 't': set(),
            'u': set(), 'v': set(), 'w': set(), 'x': set(), 'y': set(),
            'z': set()}

def get_encrypted_wordmaps(encrypted_words):
    # List to store the wordmaps in
    encrypted_wordmaps = []

    # Looping through every encrypted word
    for encrypted_word in encrypted_words:
        i = 0
        # Dict to hold the mappings of letter to integer
        mapping_dict = {}
        # Tuple to hold the work-in-progress wordmap
        mapping = ()
        # Checking every letter in the word
        for char in encrypted_word:
            if char not in mapping_dict:
                mapping_dict[char] = i
                i += 1
            mapping += (mapping_dict[char],)
        # Add the recently created wordmap for a single word
        # to the big list with all words
        encrypted_wordmaps.append(mapping)

    return tuple(encrypted_wordmaps)

def create_intersect_from_wordmaps(encrypted_words, encrypted_wordmaps):
    # Initialize the intersect where all of the lettermaps are to be combined
    intersect = get_empty_lettermapping()

    # Looking at every encrypted word one at a time
    for encrypted_word, encrypted_wordmap in zip(encrypted_words, encrypted_wordmaps):
        # Get empty lettermapping to use for this specific word
        lettermapping = get_empty_lettermapping()
        # If wordmap for the current word exists in all_wordmaps...
        if encrypted_wordmap in all_wordmaps:
            # ... go through all of the potetial candidates
            for candidate in all_wordmaps[encrypted_wordmap]:
                for cand_char, enc_char in zip(candidate, encrypted_word):
                    if cand_char not in lettermapping[enc_char]:
                        lettermapping[enc_char].add(cand_char)
        # Via the function "combine_lettermappings", combine the existing combined intersected
        # lettermapping with the newly generated one and save it as the new intersect
        intersect = combine_lettermappings(intersect, lettermapping)

    return intersect

def combine_lettermappings(mapA, mapB):
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

def remove_solved(intersect):
    solvedletters = ()
    # Add the "solved" letters to a tuple
    for letter in intersect:
        if len(intersect[letter]) == 1:
            solvedletters += (list(intersect[letter])[0],)
    # Use that tuple to remove its contents from the unsolved letters in the lettermapping
    for letter in intersect:
        if len(intersect[letter]) > 1:
            for solvedletter in solvedletters:
                if solvedletter in intersect[letter]:
                    intersect[letter].remove(solvedletter)
    return intersect

def decrypt_and_check(intersect):
    # Get statistics for the decryption
    correct = 0
    incat = 0
    zeroes = 0
    ones = 0
    certainty = -26
    for letter, candidates in intersect.items():
        if len(candidates) == 0:
            certainty += 26
            zeroes += 1
            continue
        else:
            certainty += len(candidates)
        if chr(ord(letter) - 1) in candidates or (letter == 'a' and 'z' in candidates):
            incat += 1
        if len(candidates) == 1:
            ones += 1
            candidate = list(candidates)[0]
            if ord(letter) == ord(candidate) + 1 or (ord(letter) == 97 and ord(candidate) == 122):
                correct += 1
                print(candidate, end='')
    # Print them!
    print("\nTotal correctly guessed:",correct, "\nAmong Candidates:",incat,
          "\nZeroes:",zeroes, "\nOnes:",ones, "\nCertainty:",certainty)

if __name__ == '__main__':
    # Get text
    with open('../utilities/encrypted_input.txt', encoding='utf-8') as f:
        txt = f.read().lower()
    # Cleanup text
    txt = txt.replace('\n', ' ')
    txt = txt.replace('-', ' ')
    txt = txt.replace('—', ' ')
    for letter in txt:
        if not letter.isalpha() and letter != ' ':
            txt = txt.replace(letter, '')

    # Extract words and remove non-ascii-words
    encrypted_words = txt.split()
    for i in range(len(encrypted_words) - 1, 0, -1):
        if not encrypted_words[i].isascii():
            encrypted_words.pop(i)
    encrypted_words = tuple(encrypted_words)

    # Get the wordmaps for the encryped words
    encrypted_wordmaps = get_encrypted_wordmaps(encrypted_words)
    # Use the encrpted words and wordmaps to create a guess and lettermapping
    finished_intersect = create_intersect_from_wordmaps(encrypted_words, encrypted_wordmaps)
    # Improve the guess by removing already solved letters from the other candidate lists they are in
    polished_intersect = remove_solved(finished_intersect)
    # Use the improved lettermapping to decrypt the text and get statistics
    decrypt_and_check(polished_intersect)

    # Print the total time for the file exeution
    print(time.time() - start)