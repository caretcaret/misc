from __future__ import print_function
from collections import defaultdict
from codecs import open
import heapq

# Goal 1: Load in the file and make a dict mapping each word to its number of
#         occurrences and other data. O(n)

# Goal 2: Generate a list of characters with mappings to its word compounds.
#         O(k^2 n) for k = number of characters, n = number of words

# Goal 3: Given a basis B of characters, find the next largest character c
#         to add to the basis that maximizes the span of the basis in the
#         word space. Record this order of c's when this algorithm is applied
#         repeatedly. Record the change span size. O(n^2)

# Goal 4: Compile the learning order of characters with the data and
#         corresponding words with its data (e.g. word compound definitions).


# Goal 1, assuming source file is SUBTLEX_CH_131210_CE.utf8 from
# http://expsy.ugent.be/subtlex-ch/ (2010)
def load(filename):
    words = {}
    with open(filename, 'r', 'utf-8') as f:
        f.readline() # skip the header
        line = f.readline()
        while line != "":
            items = line.strip().split('\t')
            word      = items[0]
            frequency = int(items[4])
            info      = items[1:4] + items[5:]
            # sometimes the file doesn't have unique rows (e.g. 'le'),
            # so we need to account for that. We'll take the first row
            # that we come across for the info
            if word in words:
                frequency = words[word][0] + frequency
                info = words[word][1]
            words[word] = (frequency, info)
            line = f.readline()
    return words

# Goal 2
def mapping(words):
    characters = defaultdict(list)
    # word compounds will be inserted as a heap so that we can heapsort words
    #later by frequency
    for word in words:
        for character in list(word):
            frequency, info = words[word]
            heapq.heappush(characters[character], (frequency, word, info))
    return characters

# Goal 3
# the number of occurrences of word known by understanding the characters in L
def num_known(L, frequency, word):
    if set(word) <= set(L): # subset
        return frequency
    return 0

def basis_order(words, characters, verbose=False):
    basis = []

    while len(basis) < len(characters):
        best_frequency, best_character = 0, ''
        # look for characters to add in the basis
        for character in characters:
            if character in basis:
                continue
            # find the count of words in our vocabulary if we know
            # the characters in basis and character
            frequency = sum(map(lambda T: # T is the triple from mapping()
                num_known(basis + [character], T[0], T[1]),
                characters[character]))
            # we only need to look through characters[character], because
            # this is where all the new words are going to come from if we
            # add the character
            if frequency > best_frequency:
                best_frequency, best_character = frequency, character

        if best_character == '':
            break
        basis.append(best_character)
        if verbose:
            print(len(basis), best_character, best_frequency)

    return basis

# Goal 4
# basis is the desired character order
def useful_info(basis, words, characters):
    count = 0
    occurrences = 0
    known = [] # characters that we know
    span = set() # words that we know
    print("""<!doctype html><html><head><meta charset="utf-8"><title>Dictionary</title></head><body><table border="1">
    <thead style="font-weight:bold"><td>Phrase</td><td>Frequency of Phrase</td>
    <td>Pronunciation</td><td>Definition</td></thead><tbody>""")
    for character in basis:
        count += 1
        known.append(character)
        new_words = []
        for frequency, word, info in characters[character]:
            if word in span or not (set(word) <= set(known)):
                continue
            span.add(word)
            new_words.append((frequency, word, info))
            occurrences += frequency
        print("<tr><td colspan=\"4\">#"+ str(count) + " <span style=\"font-size:36px\">" + character + '</span> ({:.4%})'.format(occurrences / 33546516) + "</td></tr>")
        for frequency, word, info in sorted(new_words, reverse=True):
            if len(info) >= 13 and info[12] != '#':
                print('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(word, str(frequency), info[1], info[12]))
    print("</tbody></table></body></html>")

"""
# Temporary calculations
def calc(filename, words):
    count = 33546516 # number of word occurrences

    with open(filename, 'r', 'utf-8') as f:
        line = f.readline().strip()
        ordering = line

    return binsearch(ordering, 0.99 * count, quality)


def quality(ordering, i):
    L = set(ordering[:i])
    count = 0
    for word in words:
        frequency, info = words[word]
        #if len(info) >= 13 and info[12] != '#':
        count += num_known(L, frequency, word)
    return count

# binary search!
def binsearch(arr, thing, quality):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        print("Trying", mid)
        q = quality(arr, mid)
        if q == thing:
            return mid
        elif q > thing:
            hi = mid
        else:
            lo = mid + 1
    return lo
"""

if __name__ == '__main__':
    FILENAME = 'SUBTLEX_CH_131210_CE.utf8'
    #print("Loading", FILENAME)
    words = load(FILENAME)
    #print("Creating character list...")
    characters = mapping(words)
    #print("Calculating learning order...")
    #basis = basis_order(words, characters, verbose=True)
    with open('character_order.txt', 'r', 'utf-8') as f:
        basis = list(f.readline().strip())
    useful_info(basis, words, characters)
    #print(calc('order.txt', words))
