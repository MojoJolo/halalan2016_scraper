import nltk.data
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from db import Db

BALANCE_NUMBER = 0.1
tokenizer = nltk.data.load('file:trainer/english.pickle')

def getSentiment(sentence):
  blob = TextBlob(sentence, analyzer=NaiveBayesAnalyzer())
  sentiment = blob.sentiment

  neg_score = sentiment.p_neg + BALANCE_NUMBER
  pos_score = sentiment.p_pos - BALANCE_NUMBER

  if pos_score < 0:
    pos_score = 0
    neg_score = 1

  return pos_score

def splitSentences(text):
  return tokenizer.tokenize(text)

def average(scores):
  print scores
  return sum(scores) / len(scores)

# ##############

articles = Db().getArticlesWithNullSentiment()

for article in articles:
  title = article['title']
  title_score = getSentiment(title)

  sentences = splitSentences(article['article'])
  article_scores = []

  for sentence in sentences:
    article_scores.append(getSentiment(sentence))

  article_score = average(article_scores)

  print title
  print title_score
  print article_score
  print article['url']