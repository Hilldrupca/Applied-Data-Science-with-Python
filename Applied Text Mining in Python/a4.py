'''
NOTE: Slightly more blobs of code provided by Coursera. Will be noted.
    


For the first part of this assignment, you will complete the functions doc_to_synsets and similarity_score which will be used by document_path_similarity to find the path similarity between two documents.

The following functions are provided:

    convert_tag: converts the tag given by nltk.pos_tag to a tag used by wordnet.synsets. You will need to use this function in doc_to_synsets.
    document_path_similarity: computes the symmetrical path similarity between two documents by finding the synsets in each document using doc_to_synsets, then computing similarities using similarity_score.

You will need to finish writing the following functions:

    doc_to_synsets: returns a list of synsets in document. This function should first tokenize and part of speech tag the document using nltk.word_tokenize and nltk.pos_tag. Then it should find each tokens corresponding synset using wn.synsets(token, wordnet_tag). The first synset match should be used. If there is no match, that token is skipped.
    similarity_score: returns the normalized similarity score of a list of synsets (s1) onto a second list of synsets (s2). For each synset in s1, find the synset in s2 with the largest similarity value. Sum all of the largest similarity values together and normalize this value by dividing it by the number of largest similarity values found. Be careful with data types, which should be floats. Missing values should be ignored.

Once doc_to_synsets and similarity_score have been completed, submit to the autograder which will run test_document_path_similarity to test that these functions are running correctly.

Do not modify the functions convert_tag, document_path_similarity, and test_document_path_similarity.
'''
import numpy as np
import pandas as pd
import nltk, pickle, gensim
import sys, os
from nltk.corpus import wordnet as wn
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# NOTE: provided by Coursera
def convert_tag(tag):
    """Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets"""
    
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
    try:
        return tag_dict[tag[0]]
    except KeyError:
        return None



'''
Returns a list of synsets in document.

Tokenizes and tags the words in the document doc.
Then finds the first synset for each word/tag combination.
If a synset is not found for that combination it is skipped.
'''
def doc_to_synsets(doc):
    """
    Args:
        doc: string to be converted

    Returns:
        list of synsets

    Example:
        doc_to_synsets('Fish are nvqjp friends.')
        Out: [Synset('fish.n.01'), Synset('be.v.01'), Synset('friend.n.01')]
    """
    tokens = nltk.word_tokenize(doc)
    tags = nltk.pos_tag(tokens)

    synsets = []
    for word, tag in tags:
        pos = convert_tag(tag)
        syn = wn.synsets(word,pos=pos)
        if syn:
            synsets.append(syn[0])
    
    return synsets



'''
Calculate the normalized similarity score of s1 onto s2

For each synset in s1, finds the synset in s2 with the largest similarity value.
Sum of all of the largest similarity values and normalize this value by dividing it by the
number of largest similarity values found.
'''
def similarity_score(s1, s2):
    """
    Args:
        s1, s2: list of synsets from doc_to_synsets

    Returns:
        normalized similarity score of s1 onto s2

    Example:
        synsets1 = doc_to_synsets('I like cats')
        synsets2 = doc_to_synsets('I like dogs')
        similarity_score(synsets1, synsets2)
        Out: 0.73333333333333339
    """
    path_score = []
    for sense_one in s1:
        temp = []
        for x in s2:
            a = sense_one.path_similarity(x)
            if a:
                temp.append(a)
        if temp:
            path_score.append(max(temp))
        
    return sum(path_score)/len(path_score)



# NOTE: provided by Coursera
def document_path_similarity(doc1, doc2):
    """Finds the symmetrical similarity between doc1 and doc2"""

    synsets1 = doc_to_synsets(doc1)
    synsets2 = doc_to_synsets(doc2)
    
    return (similarity_score(synsets1, synsets2) + similarity_score(synsets2, synsets1)) / 2



'''
Use this function to check if doc_to_synsets and similarity_score are correct.

This function should return the similarity score as a float.
'''
# NOTE: provided by Coursera
def test_document_path_similarity():
    doc1 = 'This is a function to test document_path_similarity.'
    doc2 = 'Use this function to see if your code in doc_to_synsets \
    and similarity_score is correct!'
    return document_path_similarity(doc1, doc2)



'''
paraphrases is a DataFrame which contains the following columns: Quality, D1, and D2.

Quality is an indicator variable which indicates if the two documents D1 and D2 are paraphrases of one another (1 for paraphrase, 0 for not paraphrase).
'''
# NOTE: provided by Coursera
# Use this dataframe for questions most_similar_docs and label_accuracy
paraphrases = pd.read_csv(sys.path[-1] + '/Data/paraphrases.csv')
paraphrases.head()



'''
Using document_path_similarity, find the pair of documents in paraphrases which has the maximum similarity score.

This function should return a tuple (D1, D2, similarity_score)
'''
def most_similar_docs():
    res = ('','',0)
    for x in paraphrases.index:
        d1 = paraphrases.iloc[x]['D1']
        d2 = paraphrases.iloc[x]['D2']
        score = document_path_similarity(d1, d2)
        if res[2] < score:
            res = (d1, d2, score)
            
    return res



'''
Provide labels for the twenty pairs of documents by computing the similarity for each pair using document_path_similarity. Let the classifier rule be that if the score is greater than 0.75, label is paraphrase (1), else label is not paraphrase (0). Report accuracy of the classifier using scikit-learn's accuracy_score.

This function should return a float.
'''
def label_accuracy():
    paraphrases['Para'] = 0
    for x in paraphrases.index:
        d1 = paraphrases.iloc[x]['D1']
        d2 = paraphrases.iloc[x]['D2']
        score = document_path_similarity(d1, d2)
        
        score = 1 if score >0.75 else 0
        
        paraphrases.loc[x,'Para'] = score
    
    return accuracy_score(paraphrases['Quality'], paraphrases['Para'])



'''
For the second part of this assignment, you will use Gensim's LDA (Latent Dirichlet Allocation) model to model topics in newsgroup_data. You will first need to finish the code in the cell below by using gensim.models.ldamodel.LdaModel constructor to estimate LDA model parameters on the corpus, and save to the variable ldamodel. Extract 10 topics using corpus and id_map, and with passes=25 and random_state=34.
'''
# NOTE: provided by Coursera
# Load the list of documents
with open(sys.path[-1] + '/Data/newsgroups', 'rb') as f:
    newsgroup_data = pickle.load(f)

# Use CountVectorizor to find three letter tokens, remove stop_words, 
# remove tokens that don't appear in at least 20 documents,
# remove tokens that appear in more than 20% of the documents
vect = CountVectorizer(min_df=20, max_df=0.2, stop_words='english', 
                       token_pattern='(?u)\\b\\w\\w\\w+\\b')
# Fit and transform
X = vect.fit_transform(newsgroup_data)

# Convert sparse matrix to gensim corpus.
corpus = gensim.matutils.Sparse2Corpus(X, documents_columns=False)

# Mapping from word IDs to words (To be used in LdaModel's id2word parameter)
id_map = dict((v, k) for k, v in vect.vocabulary_.items())



'''
Use the gensim.models.ldamodel.LdaModel constructor to estimate 
LDA model parameters on the corpus, and save to the variable `ldamodel`
'''
ldamodel = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id_map)



'''
Using ldamodel, find a list of the 10 topics and the most significant 10 words in each topic. This should be structured as a list of 10 tuples where each tuple takes on the form:

(9, '0.068*"space" + 0.036*"nasa" + 0.021*"science" + 0.020*"edu" + 0.019*"data" + 0.017*"shuttle" + 0.015*"launch" + 0.015*"available" + 0.014*"center" + 0.014*"sci"')

for example.

This function should return a list of tuples.
'''
def lda_topics():
    return ldamodel.show_topics(num_topics=10)



# NOTE: new_doc provided by Coursera
new_doc = ["\n\nIt's my understanding that the freezing will start to occur because \
of the\ngrowing distance of Pluto and Charon from the Sun, due to it's\nelliptical orbit. \
It is not due to shadowing effects. \n\n\nPluto can shadow Charon, and vice-versa.\n\nGeorge \
Krumins\n-- "]



'''
For the new document new_doc, find the topic distribution. Remember to use vect.transform on the the new doc, and Sparse2Corpus to convert the sparse matrix to gensim corpus.

This function should return a list of tuples, where each tuple is (#topic, probability)
'''
def topic_distribution():
    X_2 = vect.transform(new_doc)
    corpus_2 = gensim.matutils.Sparse2Corpus(X_2, documents_columns=False)
    lda = ldamodel.top_topics(corpus=corpus_2)

    return [(z[1],z[0]) for x in lda for y in x if isinstance(y,list) for z in y][:10]



'''
From the list of the following given topics, assign topic names to the topics you found. If none of these names best matches the topics you found, create a new 1-3 word "title" for the topic.

Topics: Health, Science, Automobiles, Politics, Government, Travel, Computers & IT, Sports, Business, Society & Lifestyle, Religion, Education.

This function should return a list of 10 strings.
'''
def topic_names():
    res = ['Automobiles','Not Old','Science','Excellent','Travel','Sports',
          'Education','Business','Automobilles','Action']
    
    # This question doesn't involve code. More thinking/judgement
    # calls according to course mentor
    
    return res
