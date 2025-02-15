import requests
import pandas as pd
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def fetch_articles():
    api_key = "ad533ac079034c2daf48616494df3601"
    start_day = date.today() - timedelta(2)
    format = '%Y-%m-%d'
    start_date = start_day.strftime(format)
    url = "https://newsapi.org/v2/everything?q=AI+Machine+Learning+Deep+Learning&from="+ start_date +"&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url).json()
    if(response['status'] != 'error') :
        return response['articles']
    else :
        print("Your API key is invalid or incorrect")
        return "error"

def scrape_article_text(url):
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join([p.text for p in paragraphs[:5]])  # First 5 paragraphs
    except:
        return ""
    

def send_email(body):
    sender = "nanotechsuresh@gmail.com"
    receiver = "nanotechsuresh@gmail.com"
    password = "fmso zzzl acjw bkzg"  # Use an app-specific password

    msg = MIMEText(body)
    msg['Subject'] = f"AI News Updates - {datetime.today().strftime('%Y-%m-%d')}"
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())


articles = fetch_articles()
df = pd.DataFrame(articles)[['title', 'url', 'publishedAt', 'source']]
df.to_csv("raw_articles.csv")

keywords = ["advancement", "breakthrough", "invention", "achievement", "discovery", "new", "milestone"]
df['relevance_score'] = df['title'].apply(lambda x: sum(keyword in x.lower() for keyword in keywords))

trusted_sources = ['MIT News', 'TechCrunch', 'Wired', 'ArXiv','Kaggle','Medium']
df['source_score'] = df['source'].apply(lambda x: 2 if x['name'] in trusted_sources else 1)
df['total_score'] = df['relevance_score'] + df['source_score']
top_5 = df.sort_values(by=['total_score', 'publishedAt'], ascending=False).head(5)

today = datetime.today().strftime('%Y-%m-%d')
top_5.to_csv(f"AI_News_{today}.csv")

# Generate email body from top_5 DataFrame
email_body = "\n".join([f"{i+1}. {row['title']} - {row['url']}" for i, row in top_5.iterrows()])
send_email(email_body)
