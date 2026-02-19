import time
import string
from monograms import monograms
from digrams import digrams

start = time.time()

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
    print("\nTotal correctly guessed:", correct, "\nAmong Candidates:", incat,
          "\nZeroes:", zeroes, "\nOnes:", ones, "\nCertainty:", certainty)

def get_empty_lettermapping():
    return {'a': [], 'b': [], 'c': [], 'd': [], 'e': [],
            'f': [], 'g': [], 'h': [], 'i': [], 'j': [],
            'k': [], 'l': [], 'm': [], 'n': [], 'o': [],
            'p': [], 'q': [], 'r': [], 's': [], 't': [],
            'u': [], 'v': [], 'w': [], 'x': [], 'y': [],
            'z': []}

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

if __name__ == '__main__':
    # Retrieve txt
    with open('../utilities/encrypted_input.txt', encoding='utf-8') as f:
        txt = f.read().lower()

    # Clean the text
    txt = txt.replace('\n', ' ')
    txt = txt.replace('-', ' ')
    txt = txt.replace('—', ' ')
    for char in txt:
        if not char.isalpha() and char != ' ':
            txt = txt.replace(char, '')

    # Get the data and lettermappings for mono- and digrams
    monograms_lettermapping, null = monograms(txt)
    digrams_lettermapping = digrams(txt)

    # Combine the results
    intersect = combine_lettermappings(monograms_lettermapping, digrams_lettermapping)

    # Polish the result by removing already solved candidate letters (letters with only 1 possible candidate letter)
    # from all other letters
    intersect = remove_solved(intersect)

    # Try to decrypt the text and calculate stastistics as well as print execution time
    decrypt_and_check(intersect)
    print(time.time() - start)