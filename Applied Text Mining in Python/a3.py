'''
In this assignment you will explore text message data and create models to predict if a message is spam or not. 
'''
import pandas as pd
import numpy as np
import sys, os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# NOTE: Following provided by Coursera
spam_data = pd.read_csv(sys.path[-1] + '/Data/spam.csv')

spam_data['target'] = np.where(spam_data['target']=='spam',1,0)
#spam_data.head(10)

X_train, X_test, y_train, y_test = train_test_split(spam_data['text'],
                                                    spam_data['target'],
                                                    random_state=0)


# NOTE: following method provided by Coursera
def add_feature(X, feature_to_add):
    '''
    Returns sparse feature matrix with added feature.
    feature_to_add can also be a list of features.
    '''
    from scipy.sparse import csr_matrix, hstack
    return hstack([X, csr_matrix(feature_to_add).T], 'csr')



'''
What percentage of the documents in spam_data are spam?

This function should return a float, the percent value (i.e. ratio∗100ratio∗100).
'''
def answer_one():
    spam_count = len(spam_data[(spam_data['target'] == 1)])
    
    return spam_count/len(spam_data)*100



'''
Fit the training data X_train using a Count Vectorizer with default parameters.

What is the longest token in the vocabulary?

This function should return a string.
'''
def answer_two():
    X_train_vectorized = CountVectorizer().fit(X_train)
    sorted_key_length = sorted(X_train_vectorized.vocabulary_.keys(),
                               key=len, reverse=True)
    
    return sorted_key_length[0]



'''
Fit and transform the training data X_train using a Count Vectorizer with default parameters.

Next, fit a fit a multinomial Naive Bayes classifier model with smoothing alpha=0.1. Find the area under the curve (AUC) score using the transformed test data.

This function should return the AUC score as a float.
'''
def answer_three():
    cv = CountVectorizer().fit(X_train)
    X_train_vectorized = cv.transform(X_train)
    multi_nb = MultinomialNB(alpha=0.1).fit(X_train_vectorized, y_train)
    predict = multi_nb.predict(cv.transform(X_test))
    
    return roc_auc_score(y_test, predict)



'''
Fit and transform the training data X_train using a Tfidf Vectorizer with default parameters.

What 20 features have the smallest tf-idf and what 20 have the largest tf-idf?

Put these features in a two series where each series is sorted by tf-idf value and then alphabetically by feature name. The index of the series should be the feature name, and the data should be the tf-idf.

The series of 20 features with smallest tf-idfs should be sorted smallest tfidf first, the list of 20 features with largest tf-idfs should be sorted largest first.

This function should return a tuple of two series (smallest tf-idfs series, largest tf-idfs series).
'''
def answer_four():
    tfidf_vect = TfidfVectorizer().fit(X_train)
    X_train_vectorized = tfidf_vect.transform(X_train)
    
    # max(0) will the maximum tf-idf for each feature, min(0) will produce
    #   the same result
    #
    # toarray() converts to an array of shape [[ x , x , x ]]
    sorted_tfidf = X_train_vectorized.max(0).toarray()[0]
    
    # argsort() sorts the results of toarray() and returns an array of sorted
    #   index values. Sorts by low-->high
    sorted_index = sorted_tfidf.argsort()
    feature_names = np.array(tfidf_vect.get_feature_names())
    
    largest_tfidf = pd.Series(data=sorted_tfidf[sorted_index[-1:-21:-1]],
                              index=feature_names[sorted_index[-1:-21:-1]])
    
    smallest_tfidf = pd.Series(data=sorted_tfidf[sorted_index[:20]],
                               index=feature_names[sorted_index[:20]])
    
    # convert largest_tfidf values to negative for descending sort
    large = largest_tfidf[np.lexsort([largest_tfidf.index, -largest_tfidf.values])]
    small = smallest_tfidf[np.lexsort([smallest_tfidf.index, smallest_tfidf.values])]

    return small, large



'''
Fit and transform the training data X_train using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than 3.

Then fit a multinomial Naive Bayes classifier model with smoothing alpha=0.1 and compute the area under the curve (AUC) score using the transformed test data.

This function should return the AUC score as a float.
'''
def answer_five():
    tfidf_vect = TfidfVectorizer(min_df=3).fit(X_train)
    X_train_vectorized = tfidf_vect.transform(X_train)
    
    multi_nb = MultinomialNB(alpha=0.1).fit(X_train_vectorized, y_train)
    predict = multi_nb.predict(tfidf_vect.transform(X_test))
    
    return roc_auc_score(y_test, predict)



'''
What is the average length of documents (number of characters) for not spam and spam documents?

This function should return a tuple (average length not spam, average length spam).
'''
def answer_six():
    spam_data['length'] = spam_data['text'].apply(func=len)
    not_spam_len = spam_data[(spam_data['target']==0)]['length']
    spam_len = spam_data[(spam_data['target']==1)]['length']
    
    return sum(not_spam_len)/len(not_spam_len), sum(spam_len)/len(spam_len)
answer_six()



'''
Fit and transform the training data X_train using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than 5.

Using this document-term matrix and an additional feature, the length of document (number of characters), fit a Support Vector Classification model with regularization C=10000. Then compute the area under the curve (AUC) score using the transformed test data.

This function should return the AUC score as a float.
'''
def answer_seven():
    tfidf_vect = TfidfVectorizer(min_df=5).fit(X_train)
    X_train_vectorized = tfidf_vect.transform(X_train)
    
    spam_train = spam_data.iloc[X_train.index]
    spam_test = spam_data.iloc[X_test.index]
    
    # add_feature method provided by coursera
    X_train_vectorized = add_feature(X_train_vectorized,
                                     spam_train['length'])
    
    X_test_vectorized = tfidf_vect.transform(X_test)
    X_test_vectorized = add_feature(X_test_vectorized,
                                    spam_test['length'])
    
    svc = SVC(C=10000).fit(X_train_vectorized, y_train)
                                    
    predict = svc.predict(X_test_vectorized)
    
    return roc_auc_score(y_test, predict)
answer_seven()



'''
What is the average number of digits per document for not spam and spam documents?

This function should return a tuple (average # digits not spam, average # digits spam).
'''
def answer_eight():
    temp = spam_data['text'].str.findall('\d')
    spam_data['digits'] = temp.apply(func=len)
    not_spam_digits = spam_data[(spam_data['target'] == 0)]
    spam_digits = spam_data[(spam_data['target'] == 1)]
    
    return not_spam_digits['digits'].sum()/len(not_spam_digits), \
           spam_digits['digits'].sum()/len(spam_digits)
answer_eight()



'''
Fit and transform the training data X_train using a Tfidf Vectorizer ignoring terms that have a document frequency strictly lower than 5 and using word n-grams from n=1 to n=3 (unigrams, bigrams, and trigrams).

Using this document-term matrix and the following additional features:

    the length of document (number of characters)
    number of digits per document

fit a Logistic Regression model with regularization C=100. Then compute the area under the curve (AUC) score using the transformed test data.

This function should return the AUC score as a float.
'''
def answer_nine():
    tfidf_vect = TfidfVectorizer(min_df=5, ngram_range=(1,3)).fit(X_train)
    X_train_vectorized = tfidf_vect.transform(X_train)
    
    spam_train = spam_data.iloc[X_train.index]
    spam_test = spam_data.iloc[X_test.index]
    
    X_train_vectorized = add_feature(X_train_vectorized,
                                     spam_train['length'])
    
    X_train_vectorized = add_feature(X_train_vectorized,
                                     spam_train['digits'])
    
    X_test_vectorized = tfidf_vect.transform(X_test)
    X_test_vectorized = add_feature(X_test_vectorized,
                                    spam_test['length'])
    
    X_test_vectorized = add_feature(X_test_vectorized,
                                    spam_test['digits'])
    
    log_reg = LogisticRegression(C=100, solver='liblinear') \
              .fit(X_train_vectorized, y_train)
    predict = log_reg.predict(X_test_vectorized)
    
    return roc_auc_score(y_test, predict)
answer_nine()



'''
What is the average number of non-word characters (anything other than a letter, digit or underscore) per document for not spam and spam documents?

Hint: Use \w and \W character classes

This function should return a tuple (average # non-word characters not spam, average # non-word characters spam).
'''
def answer_ten():
    temp = spam_data['text'].str.findall('\W')
    spam_data['non-word'] = temp.apply(func=len)
    not_spam_non = spam_data[(spam_data['target'] == 0)]
    spam_non = spam_data[(spam_data['target'] == 1)]
    
    
    return sum(not_spam_non['non-word'])/len(not_spam_non), \
           sum(spam_non['non-word'])/len(spam_non)
answer_ten()



'''
Fit and transform the training data X_train using a Count Vectorizer ignoring terms that have a document frequency strictly lower than 5 and using character n-grams from n=2 to n=5.

To tell Count Vectorizer to use character n-grams pass in analyzer='char_wb' which creates character n-grams only from text inside word boundaries. This should make the model more robust to spelling mistakes.

Using this document-term matrix and the following additional features:

    the length of document (number of characters)
    number of digits per document
    number of non-word characters (anything other than a letter, digit or underscore.)

fit a Logistic Regression model with regularization C=100. Then compute the area under the curve (AUC) score using the transformed test data.

Also find the 10 smallest and 10 largest coefficients from the model and return them along with the AUC score in a tuple.

The list of 10 smallest coefficients should be sorted smallest first, the list of 10 largest coefficients should be sorted largest first.

The three features that were added to the document term matrix should have the following names should they appear in the list of coefficients: ['length_of_doc', 'digit_count', 'non_word_char_count']

This function should return a tuple (AUC score as a float, smallest coefs list, largest coefs list).
'''
def answer_eleven():
    cv = CountVectorizer(min_df=5, ngram_range=(2,5), analyzer='char_wb').fit(X_train)
    X_train_vectorized = cv.transform(X_train)
    
    spam_train = spam_data.iloc[X_train.index]
    spam_test = spam_data.iloc[X_test.index]
    
    train_add = [spam_train['length'], spam_train['digits'], spam_train['non-word']]
    test_add = [spam_test['length'], spam_test['digits'], spam_test['non-word']]
    
    X_train_vectorized = add_feature(X_train_vectorized,
                                     train_add)
    
    X_test_vectorized = cv.transform(X_test)
    X_test_vectorized = add_feature(X_test_vectorized,
                                    test_add)
    
    log_reg = LogisticRegression(C=100, solver='liblinear') \
              .fit(X_train_vectorized, y_train)
    predict = log_reg.predict(X_test_vectorized)

    features = cv.get_feature_names()
    features.append('length_of_doc')
    features.append('digit_count')
    features.append('non_word_char_count')
    coef_series = pd.Series(data=log_reg.coef_[0], index=features).sort_values()
    
    return roc_auc_score(y_test, predict), \
           coef_series[:10], \
           coef_series[-1:-11:-1]
answer_eleven()
