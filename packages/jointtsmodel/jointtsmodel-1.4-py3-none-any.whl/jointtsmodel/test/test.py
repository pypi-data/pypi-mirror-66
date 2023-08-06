"""
(c) Ayan Sengupta - 2020
License: MIT License

Testing of joint topic-sentiment models

"""

# Author: Ayan Sengupta

from jointtsmodel.RJST import RJST
from jointtsmodel.JST import JST
from jointtsmodel.sLDA import sLDA
from jointtsmodel.TSM import TSM

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from jointtsmodel.utils import *
# This produces a feature matrix of token counts, similar to what
# CountVectorizer would produce on text.
data, _ = fetch_20newsgroups(shuffle=True, random_state=1,
                         remove=('headers', 'footers', 'quotes'),
                         return_X_y=True)
data = data[:1000]
vectorizer = CountVectorizer(max_df=0.7, min_df=10,
                            max_features=5000,
                            stop_words='english')
X = vectorizer.fit_transform(data)
vocabulary = vectorizer.get_feature_names()
inv_vocabulary = dict(zip(vocabulary,np.arange(len(vocabulary))))
lexicon_data = pd.read_excel('lexicon/prior_sentiment.xlsx')
lexicon_data = lexicon_data.dropna()
lexicon_dict = dict(zip(lexicon_data['Word'],lexicon_data['Sentiment']))

### RJST model ###
model = RJST(n_topic_components=5,n_sentiment_components=5,random_state=123,evaluate_every=2)
model.fit(X.toarray(), lexicon_dict)

model.transform()[:2]

top_words = list(model.getTopKWords(vocabulary).values())
coherence_score_uci(X.toarray(),inv_vocabulary,top_words)
Hscore(model.transform())

### TSM ###
model = TSM(n_topic_components=5,n_sentiment_components=5,random_state=123,evaluate_every=2)
model.fit(X.toarray(), lexicon_dict)

model.transform()[:2]

top_words = list(model.getTopKWords(vocabulary).values())
coherence_score_uci(X.toarray(),inv_vocabulary,top_words)
Hscore(model.transform())

### JST model ###
model = JST(n_topic_components=5,n_sentiment_components=5,random_state=123,evaluate_every=2)
model.fit(X.toarray(), lexicon_dict)

model.transform()[:2]

top_words = list(model.getTopKWords(vocabulary).values())
coherence_score_uci(X.toarray(),inv_vocabulary,top_words)
Hscore(model.transform())

### sLDA model ###
model = sLDA(n_topic_components=5,n_sentiment_components=5,random_state=123,evaluate_every=2)
model.fit(X.toarray(), vocabulary)

model.transform()[:2]

top_words = list(model.getTopKWords(vocabulary).values())
coherence_score_uci(X.toarray(),inv_vocabulary,top_words)
Hscore(model.transform())