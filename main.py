from textblob import TextBlob
from googletrans import Translator, constants
from pprint import pprint

translator = Translator()

text = """Jeg hater deg din stygge fisk"""

translation = translator.translate(text)

text = translation.text
print(text)

blob = TextBlob(text)

for sentence in blob.sentences:
    print(f"Sentiment: {sentence.sentiment.polarity}")



