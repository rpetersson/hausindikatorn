#from textblob import TextBlob
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium import webdriver
from datetime import datetime, timedelta
import concurrent.futures

MAX_THREADS = 1
list_result = []

from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "./chromedriver.exe"

options = Options()
options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

analyzer = SentimentIntensityAnalyzer()

# URL

max_sidor = 30 # Max antal sidor den ska gå igenom
url_to_forum = "https://www.avanza.se/placera/forum/forum/synact-pharma."


def generatePages(max_sidor, url_to_forum):
    list_with_url = []
    link = 0
    for i in range(max_sidor):
        link = link + 15
        list_with_url.append(url_to_forum + str(link) + ".html")
    return list_with_url

def scrape(url):
    driver.get(url)
    print(url)
    poster = driver.find_elements_by_class_name("userPost")
    for text in poster:  # Går igenom post för post.
        try:

            vs = analyzer.polarity_scores(text.text)
            sentiment_per_post = vs["compound"]

            # Ordna med tider...
            datum = text.text.splitlines()[1]
            # datum = str(datum[0:10])
            if "igår" in datum:
                datum = datetime.today().date() - timedelta(days=1)
            if "idag" in datum:
                datum = datetime.today().date()

           # with open("result_file.csv", "w") as file:
            #    file.writelines(str(datum) + ","+str(sentiment_per_post))

            list_result.append(str(datum) + ","+str(sentiment_per_post))

        except Exception as e:
            print(e)
            list_result.append("Exception...")




if __name__ == '__main__':

    all_url = generatePages(max_sidor, url_to_forum)
    print(all_url)
    threads = min(MAX_THREADS, len(all_url))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(scrape, all_url)

    with open("result_file.csv", "w") as file:
        for i in list_result:
            file.writelines(i + "\n")





