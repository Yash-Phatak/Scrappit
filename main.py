import pyrebase
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#Setting the firebase configurations
config = {
    "apiKey": "AIzaSyA2rGBnxAPEcHpd6xWKy4zZw9rUIy8nFgs",
    "authDomain": "scrap-802a1.firebaseapp.com",
    "databaseURL": "https://scrap-802a1-default-rtdb.firebaseio.com",
    "projectId": "scrap-802a1",
    "storageBucket": "scrap-802a1.appspot.com",
    "messagingSenderId": "861765380428",
    "appId": "1:861765380428:web:454c0d2b5653be6fd047e9",
    "measurementId": "G-BQSMMQMJ71"
}
firebase = pyrebase.initialize_app(config)

#Getting Reference to Database Service
db = firebase.database()

#define scraper function
def scraper():
    start = "https://news.google.com/search?q="
    query = "covid".split()
    query_separator = "%20".join(query)
    end = "&hl=en-IN&gl=IN&ceid=IN%3Aen"
    url = start+query_separator+end

    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.content,'html.parser') #will try lxml also
    headlines = soup.find_all('a')
    all_headlines ={}
    count =0
    for headline in headlines:
        if count<9:
            key = "0"+str(count)
        else:
            key = str(count)
        all_headlines[key] = headline.text
        count+=1
    
    now = datetime.now()
    current_date = now.strftime("%d")
    current_month= now.strftime("%B")
    current_year = now.strftime("%Y")

    db.child("Covid Headlines").child(current_year).child(current_month).child(current_date).set(all_headlines)

#Defining the Scheduler Function
def scheduler():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # Trigger scraper function everyday on 12 AM
    if current_time == "00:00:00":
        scraper()

scheduler()