from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

sentence = "Aquino, Purisima, Napenas liable for Mamasapano"
print sentence

blob = TextBlob(sentence, analyzer=NaiveBayesAnalyzer())
print blob.sentiment

blob = TextBlob(sentence)
print blob.sentiment