import requests
from matplotlib import pyplot as plt
import smtplib

DAILY_CLOSING_PRICE = []
closing_data = []
dates_data = []

FROMADDR = "From address"
TOADDR = "to address"

PASSWORD = "pass"

def send_news(d,per):
    
    news_url = f"https://newsapi.org/v2/everything?q=Tesla Inc&from={d}&sortBy=popularity&apiKey=demo
    news_req = requests.get(news_url)
    news_data = news_req.json()
    news_articles = news_data["articles"][:3]
    
    for article in news_articles:
        news_headline = article["title"]
        news_description = article["description"]
        
        msg = f"Subject: {per}| Daily News {news_headline}\n\n{news_description}"
        
        with smtplib.SMTP('smtp.gmail.com',587,timeout=120) as server:
            
            server.ehlo()
            server.starttls()
            
            server.ehlo()
            
        
            server.login(FROMADDR, PASSWORD)
            server.sendmail(FROMADDR, TOADDR, msg.encode('ascii', 'ignore').decode('ascii'))
    

url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&interval=5min&apikey=demo"
r = requests.get(url)
data = r.json()

time_series_data = data["Time Series (Daily)"]


for key,values in time_series_data.items():
    
    closing_price=values["4. close"]
    daily_data = {
        "date": key,
        "closing_price":int(float(closing_price))
        }
    closing_data.append(int(float(closing_price)))
    dates_data.append(key)
    DAILY_CLOSING_PRICE.append(daily_data)



plt.title("Plotting closing prices per day")
plt.xlabel("Dates")
plt.ylabel("Closing Prices")
plt.xticks(rotation=90)
plt.plot(dates_data,closing_data , color="blue" , marker="o")
plt.show()

today_price=DAILY_CLOSING_PRICE[0]["closing_price"]
yes_price = DAILY_CLOSING_PRICE[1]["closing_price"]
closing_date = DAILY_CLOSING_PRICE[0]["date"]

difference = today_price - yes_price

if difference > 0:
    
    positive_difference = abs(difference)
    percentage = (positive_difference / yes_price ) *100
    answer = round(percentage)
    percent = f"TSLA Rises by 🔺{answer}%"
    if answer > 4:
        send_news(closing_data,percent)
            
else:
    negative_difference = abs(difference)
    percentage = (negative_difference / yes_price ) *100 
    answer = round(percentage)
    percent = f"TSLA drops by🔻{answer}%"
    
    if answer >4:
        send_news(closing_data,percent)
