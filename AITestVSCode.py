import requests
api_key = "ad533ac079034c2daf48616494df3601"
url = f"https://newsapi.org/v2/everything?q=AI+Machine+Learning+Deep+Learning&sortBy=publishedAt&pageSize=20&apiKey={api_key}"
response = requests.get(url).json()
articles = response['articles']
print(articles[0]['title'])  # Test if it works
