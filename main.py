from textblob import TextBlob
from googletrans import Translator
from selenium import webdriver
from datetime import datetime, timedelta

driver = webdriver.PhantomJS()

translator = Translator()

# URL
sidor = 1 #Startar på forumets sida 1.
max_sidor = str(15) # Max antal sidor den ska gå igenom.
number_of_posts = 0
sentiment = 0
list_of_hauss = []

while int(sidor) <= int(max_sidor):
    synact = "https://www.avanza.se/placera/forum/forum/synact-pharma." + str(sidor) + ".html"
    url = synact
    driver.get(url)
    print(url)
    poster = driver.find_elements_by_class_name("userPost") #Tar texten från classen userPost och sparar i ett objekt
    for text in poster: # Går igenom post för post.
        try:
            translation = translator.translate(text.text)  # Översätter med Google API
            print(text.text)
            translated_text = translation.text  # Lagrar översatt text i ny variabel.
            blob = TextBlob(translated_text)  # Tar den översatta texten och kör den i textBlob för att analysera.
            sentiment_per_post = blob.sentiment[0]  # Lagrar sentimentet i ny variabel. "fe.x: 0.001"
            sentiment = sentiment + sentiment_per_post  # Lägger ihop sentimentet för varje post.
            number_of_posts = number_of_posts + 1  # Counter för antal poster den har analyserat.
            list_of_hauss.append(sentiment_per_post)

            #Ordna med tider...
            datum = text.text.splitlines()[1]
            if "igår" in datum:
                datum = datetime.today().date() - timedelta(days=1)
            if "idag" in datum:
                datum = datetime.today().date()

        except Exception as e:
            print(e)

    sidor = sidor + 1

print("Antall poster: ", number_of_posts)
print("Håsindex: ", sentiment)
print("Genomsnitts hås", sentiment / number_of_posts)
print(list_of_hauss)













