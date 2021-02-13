from textblob import TextBlob
from googletrans import Translator
from selenium import webdriver

driver = webdriver.PhantomJS()

translator = Translator()

# URL
side = 1
max_side = str(10)

number_of_posts = 0
sentiment = 0
array_of_hauss = []

while int(side) <= int(max_side):
    synact = "https://www.avanza.se/placera/forum/forum/synact-pharma." + str(side) + ".html"
    url = synact
    driver.get(url)
    print(url)
    poster = driver.find_elements_by_class_name("userPost")

    for text in poster:

        translation = translator.translate(text.text)
        translated_text = translation.text
        blob = TextBlob(translated_text)

        for sentence in blob.sentences:
            number_of_posts = number_of_posts + 1
            #print(number_of_posts)
            sentiment_per_post = sentence.sentiment.polarity
            sentiment = sentiment + float(sentiment_per_post)
            array_of_hauss.append(sentiment_per_post)
    side = side + 1

print("Antall poster: ", number_of_posts)
print("Håsindex: ", sentiment)

print("Genomsnitts hås", sentiment / number_of_posts)
print(array_of_hauss)













