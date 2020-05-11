'''
In part 1 of this assignment you will use nltk to explore the Herman Melville novel Moby Dick. Then in part 2 you will create a spelling recommender function that uses nltk to find words similar to the misspelling. 
'''
import nltk, sys, os
import pandas as pd
import numpy as np
from nltk.corpus import words



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
nltk.data.path.append(sys.path[-1])



__author__ = 'Chris Hilldrup'



# NOTE: following provided by coursera
'''
Part 1

If you would like to work with the raw text you can use 'moby_raw'
'''
with open(sys.path[-1] + '/Data/moby.txt', 'r') as f:
    moby_raw = f.read()
    
# If you would like to work with the novel in nltk.Text format you can use 'text1'
moby_tokens = nltk.word_tokenize(moby_raw)
text1 = nltk.Text(moby_tokens)



'''
What is the lexical diversity of the given text input? (i.e. ratio of unique tokens to the total number of tokens)

This function should return a float.
'''
def answer_one():    
    return len(set(moby_tokens))/len(moby_tokens)



'''
What percentage of tokens is 'whale'or 'Whale'?

This function should return a float.
'''
def answer_two():
    dist = nltk.probability.FreqDist(text1)
    
    return (dist['whale'] + dist['Whale'])/len(moby_tokens)*100



'''
What are the 20 most frequently occurring (unique) tokens in the text? What is their frequency?

This function should return a list of 20 tuples where each tuple is of the form (token, frequency). The list should be sorted in descending order of frequency.
'''
def answer_three():
    dist = nltk.probability.FreqDist(text1)
    
    return dist.most_common(20)



'''
What tokens have a length of greater than 5 and frequency of more than 150?

This function should return an alphabetically sorted list of the tokens that match the above constraints. To sort your list, use sorted()
'''
def answer_four():
    dist = nltk.probability.FreqDist(text1)
    token_list = [x for x in dist if len(x)>5 and dist[x]>150]
    
    return sorted(token_list)



'''
Find the longest word in text1 and that word's length.

This function should return a tuple (longest_word, length).
'''
def answer_five():
    dist = nltk.probability.FreqDist(text1)
    sort_length = sorted(dist, key=lambda x: len(x), reverse=True)
    word = sort_length[0]
    
    return (word, len(word))



'''
What unique words have a frequency of more than 2000? What is their frequency?

"Hint: you may want to use isalpha() to check if the token is a word and not punctuation."

This function should return a list of tuples of the form (frequency, word) sorted in descending order of frequency.
'''
def answer_six():
    dist = nltk.probability.FreqDist(text1)
    word_list = [(y,x) for x,y in dist.items() if x.isalpha() and y>2000]
    
    return sorted(word_list, reverse=True)



'''
What is the average number of tokens per sentence?

This function should return a float.
'''
def answer_seven():
    sent = nltk.tokenize.sent_tokenize(moby_raw)
    word_tokens = [len(nltk.word_tokenize(x)) for x in sent]
    
    return sum(word_tokens)/len(word_tokens) 



'''
What are the 5 most frequent parts of speech in this text? What is their frequency?

This function should return a list of tuples of the form (part_of_speech, frequency) sorted in descending order of frequency.
'''
def answer_eight():
    sent = nltk.tokenize.sent_tokenize(moby_raw)
    tags = nltk.tag.pos_tag_sents([nltk.tokenize.word_tokenize(x) for x in sent])
    tag_count = {}

    for c,d in [a for b in tags for a in b]:
        if tag_count.get(d):
            tag_count[d] += 1
        else:
            tag_count[d] = 1
    
    return sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:5]



'''
Part 2

For this part of the assignment you will create three different spelling recommenders, that each take a list of misspelled words and recommends a correctly spelled word for every word in the list.

For every misspelled word, the recommender should find find the word in correct_spellings that has the shortest distance*, and starts with the same letter as the misspelled word, and return that word as a recommendation.

*Each of the three different recommenders will use a different distance measure (outlined below).

Each of the recommenders should provide recommendations for the three default words provided: ['cormulent', 'incendenece', 'validrate'].
'''



# NOTE: follow line provided by coursera
correct_spellings = words.words()



'''
For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:

Jaccard distance on the trigrams of the two words.

This function should return a list of length three: ['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation'].
'''
def answer_nine():
    res = []
    for miss in ['cormulent','incendenece','validrate']:
        tri_miss = set(nltk.trigrams(miss))
        temp = (1.0,'')
        
        for word in correct_spellings:
            if word[0] == miss[0]:
                tri_correct = set(nltk.trigrams(word))
                jd = nltk.jaccard_distance(tri_miss, tri_correct)
                if temp[0]>jd:
                    temp =(jd, word)
        
        res.append(temp)
        
    return [x[1] for x in res]



'''
For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:

Jaccard distance on the 4-grams of the two words.

This function should return a list of length three: ['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation'].
'''
def answer_ten():
    res = []
    for miss in ['cormulent','incendenece','validrate']:
        tri_miss = set(nltk.ngrams(miss, n=4))
        temp = (1.0,'')
        
        for word in correct_spellings:
            if word[0] == miss[0]:
                tri_correct = set(nltk.ngrams(word, n=4))
                jd = nltk.jaccard_distance(tri_miss, tri_correct)
                if temp[0]>jd:
                    temp =(jd, word)
        
        res.append(temp)
        
    return [x[1] for x in res]



'''
For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:

Edit distance on the two words with transpositions.

This function should return a list of length three: ['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation'].
'''
def answer_eleven():
    res = []
    for miss in ['cormulent','incendenece','validrate']:
        temp = (1000,'')
        
        for word in correct_spellings:
            if word[0] == miss[0]:
                jd = nltk.edit_distance(miss, word, transpositions=True)
                if temp[0]>jd:
                    temp =(jd, word)
        
        res.append(temp)
        
    return [x[1] for x in res]
