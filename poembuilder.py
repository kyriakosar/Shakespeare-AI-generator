import syllapy
import os
import nltk
import random
from tqdm import tqdm

# nltk.download('cmudict')

filename = 'shakespeare.txt'
n = 3
common_n = 2
rhyming_level = 2

# flag_complete rules:
#  -1 - cant find endings (comes only from buildLineWithRhyme() function)
#   0 - line not complete
#   1 - complete line


def countWordSyllables(word):
    return syllapy.count(word)

def countPhraseSyllables(phrase):
    total_syllables = 0
    words = phrase.split(' ')
    for word in words:
        total_syllables += countWordSyllables(word)
    return total_syllables

def countListSyllables(word_list):
    total_syllables = 0
    for word in word_list:
        total_syllables += countWordSyllables(word)
    return total_syllables
    
def getInspirationSet(filename):
    file = os.path.dirname(__file__) + f'/data/{filename}'
    file_handler = open(file, 'r')
    lines = file_handler.readlines()
    file_handler.close()
    return lines

def getNgrams(text, n):
    ngrams, starting_ngrams = list(), list()
    for line in text:
        ngrams_line = nltk.ngrams(line.split(), n)
        ngrams_line = list(ngrams_line)
        ngrams += ngrams_line
        starting_ngrams.append(ngrams_line[0])
    return ngrams, starting_ngrams

def getCommonPart(line, common_n, forward):
    '''
    returns the list of words that should match (search to the building line)
    '''
    starts_with, ends_with = list(), list()
    if forward:
        for i in range(common_n,0,-1):
            starts_with.append(line[-i])
        return starts_with
    else:
        for i in range(common_n):
            ends_with.append(line[i])
        return ends_with

def findPossibleNgrams(line, common_n, ngrams, forward):
    ''' 
    returns list of lists -- each list is a possible ngram that can complete the line
    '''
    possible_ngrams = list()
    common_part = getCommonPart(line, common_n, forward)
    if forward:
        for ngram in ngrams:
            ngram = list(ngram)
            if ngram[:common_n] == common_part:
                possible_ngrams.append(ngram)
    else:
        for ngram in ngrams:
            ngram = list(ngram)
            if ngram[-common_n:] == common_part:
                possible_ngrams.append(ngram)
    return possible_ngrams

def findManualNextWords(lines, word):
    next_words = dict()
    for line in lines:
        words = line.split(' ')
        if word in words:
            if words[words.index(word)+1] in next_words.keys():
                next_words[words[words.index(word)+1]] += 1
            else:
                next_words[words[words.index(word)+1]] = 1
    return list(next_words.keys()), list(next_words.values())

def buildLine(ngrams, starting_ngrams, lines, forward):
    flag_complete = 0
    num_syllables = 0
    line = list()
    current_starting_ngram = random.choice(starting_ngrams)
    line += current_starting_ngram
    num_syllables = countListSyllables(line)

    while num_syllables<10:
        possible_ngrams = findPossibleNgrams(line, common_n, ngrams, forward)
        weights = [1] * len(possible_ngrams)
        if len(possible_ngrams) == 0:   # possible ngrams of length common_n not compatible with ngrams
            possible_ngrams, weights = findManualNextWords(lines, line[-1])
        if len(possible_ngrams) == 0:
            break 
        current_ngram = random.choices(population=possible_ngrams, weights=weights, k=1)
        current_ngram = current_ngram[0]
        if isinstance(current_ngram, str):
            if '.' in current_ngram:
                line.append(current_ngram.strip().lower().replace('.', ''))
            else:
                line.append(current_ngram.strip().lower())
        else:
            token = current_ngram[-(n-common_n)]
            if '.' in token:
                line.append(token.strip().lower().replace('.', ''))
            else:
                line.append(token.strip().lower())
        num_syllables = countListSyllables(line)

    if num_syllables == 10:
        flag_complete = 1
    else:
        flag_complete = 0

    return line, flag_complete

def getRhymingWords(inp, level, lines):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]

    rhymes = set(rhymes)
    rhymes_weights = dict()
    for rhyme in rhymes:
        rhymes_weights[rhyme] = 0

    for line in lines:
        words = line.split(' ')
        words = set(words)
        intersection = words.intersection(rhymes)
        if len(intersection) > 0:
            for intersection_word in intersection:
                rhymes_weights[intersection_word] += 1

    keys_to_delete = list()
    for key, value in rhymes_weights.items():
        if value == 0:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del rhymes_weights[key]
        
    return list(rhymes_weights.keys()), list(rhymes_weights.values())

def findManualPreviousWords(lines, word):
    previous_words = dict()
    for line in lines:
        words = line.split(' ')
        if word in words:
            if words[words.index(word)-1] in previous_words.keys():
                previous_words[words[words.index(word)-1]] += 1
            else:
                previous_words[words[words.index(word)-1]] = 1
    return list(previous_words.keys()), list(previous_words.values())

def buildLineWithRhyme(ngrams, lines, word, forward):
    flag_complete = 0
    num_syllables = 0
    line = list()
    endings, weights = getRhymingWords(word, rhyming_level, lines)
    if len(endings) == 1 and endings[0] == word:
        endings, weights = getRhymingWords(word, rhyming_level-1, lines)
    if not endings:
        return line, -1
    current_ending_word = random.choices(population=endings, weights=weights, k=1)
    line += current_ending_word
    current_prevending_words, current_prevending_words_weights = findManualPreviousWords(lines, line[-1])
    chose_prevending_word = random.choices(population=current_prevending_words, weights=current_prevending_words_weights, k=1)
    line.insert(0, chose_prevending_word[0].lower())
    num_syllables = countListSyllables(line)

    while num_syllables<10:
        possible_ngrams = findPossibleNgrams(line, common_n, ngrams, forward)
        weights = [1] * len(possible_ngrams)
        if len(possible_ngrams) == 0:   # possible ngrams of length common_n not compatible with ngrams
            possible_ngrams, weights = findManualPreviousWords(lines, line[0])
        if len(possible_ngrams) == 0:
            break 
        current_ngram = random.choices(population=possible_ngrams, weights=weights, k=1)
        current_ngram = current_ngram[0]
        if isinstance(current_ngram, str):
            if '.' in current_ngram:
                line.insert(0,current_ngram.strip().lower().replace('.', ''))
            else:
                line.insert(0,current_ngram.strip().lower())
        else:
            token = current_ngram[(n-common_n)-1]
            if '.' in token:
                line.insert(0,token.strip().lower().replace('.', ''))
            else:
                line.insert(0,token.strip().lower())
        num_syllables = countListSyllables(line)

    if num_syllables == 10:
        flag_complete = 1
    else:
        flag_complete = 0

    return line, flag_complete

def createStanza(ngrams, starting_ngrams, lines):
    flag_complete_l1, flag_complete_l3 = 0, -1
    while flag_complete_l3 == -1 or flag_complete_l1 == 0 or flag_complete_l3 == 0:
        l1, flag_complete_l1 = buildLine(ngrams, starting_ngrams, lines, True)
        l3, flag_complete_l3 = buildLineWithRhyme(ngrams, lines, l1[-1], False)

    flag_complete_l2, flag_complete_l4 = 0, -1
    while flag_complete_l4 == -1 or flag_complete_l2 == 0 or flag_complete_l4 == 0:
        l2, flag_complete_l2 = buildLine(ngrams, starting_ngrams, lines, True)
        l4, flag_complete_l4 = buildLineWithRhyme(ngrams, lines, l2[-1], False)

    return l1, l2, l3, l4

def createCouplet(ngrams, starting_ngrams, lines):
    flag_complete_l1, flag_complete_l2 = 0, -1
    while flag_complete_l2 == -1 or flag_complete_l1 == 0 or flag_complete_l2 == 0:
        l1, flag_complete_l1 = buildLine(ngrams, starting_ngrams, lines, True)
        l2, flag_complete_l2 = buildLineWithRhyme(ngrams, lines, l1[-1], False)

    return l1, l2

def outputPoem(output_lines):
    poem = ''
    for line in output_lines:
        verse = f'{" ".join(line)}'
        poem += verse + '\n'
    return poem

if __name__ == '__main__':
    lines = getInspirationSet(filename)
    ngrams, starting_ngrams = getNgrams(lines, n)

    print(getRhymingWords('that',2,lines))

    # for i in tqdm(range(10)):
    #     l1, l2, l3, l4 = createStanza(ngrams, starting_ngrams, lines)
    #     l5, l6, l7, l8 = createStanza(ngrams, starting_ngrams, lines)
    #     l9, l10, l11, l12 = createStanza(ngrams, starting_ngrams, lines)
    #     l13, l14 = createCouplet(ngrams, starting_ngrams, lines)
    #     output_lines = l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14
    #     print(outputPoem(output_lines))   

    #     f = open('generated_poems.txt', 'a', encoding="utf-8")
    #     f.write(outputPoem(output_lines))
    #     f.write('\n')
    #     f.write('_' * 100)
    #     f.write('\n')
    #     f.close()