# pyenv activate pystock-3.11.2
import datetime
import dotenv
import numpy
import os
import requests

# TODO Prompt user for stock symbol and automatically return price and news
# TODO Create a GUI

# Constants
dotenv.load_dotenv()

ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query?"
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")

NEWS_API_ENDPOINT = "https://newsapi.org/v2/top-headlines?"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")


# Variables
stock_function = "TIME_SERIES_DAILY_ADJUSTED"
stock_symbol = "AAPL"
stock_params = {"function": stock_function,
          "symbol": stock_symbol,
          "apikey": ALPHA_VANTAGE_API_KEY,
          }

news_country = "us"
news_category = "business"
news_q = "apple"
news_pageSize = 5
news_params = {"country": news_country,
               "category": news_category,
               "q": news_q,
               "pageSize": news_pageSize,
               "apiKey": NEWS_API_KEY,
               }


yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
yesterday_str = yesterday_date.strftime("%Y-%m-%d")


# Functions
def request_stock_info() -> dict:
    response = requests.get(ALPHA_VANTAGE_ENDPOINT,
                            params=stock_params)
    response.raise_for_status()
    return response.json()["Time Series (Daily)"][yesterday_str]

def request_news_info() -> dict:
    response = requests.get(NEWS_API_ENDPOINT,
                            params=news_params)
    response.raise_for_status()
    return response.json()

def add_positive_sign(price) -> str:
    return "{0:{1}}".format(price, "+" if price else "")

def extract_headlines(news_response_dict) -> list:
    list = news_response_dict["articles"]
    return [article["title"] for article in list]

def print_headlines(list_headlines) -> None:
    index = 0
    for i in list_headlines:
        index += 1
        print(f"{index}. {i}")
    
def main() -> None:
   stocks_response_dict = request_stock_info()
   news_response_dict = request_news_info()
   
   open_price = float(stocks_response_dict["1. open"])
   high_price = float(stocks_response_dict["2. high"])
   low_price = float(stocks_response_dict["3. low"])
   close_price = float(stocks_response_dict["4. close"])
   difference_price = numpy.around(close_price - low_price, 2)
   difference_price_str = add_positive_sign(difference_price)
   difference_percent = numpy.around(difference_price / close_price, 3) * 100
   difference_percent_str = add_positive_sign(difference_percent)
   
   print(f"\nExchange for {stock_symbol} on {yesterday_str}\n"
         f"Open: {open_price}\n"
         f"Close: {close_price}\n"
         f"High: {high_price}\n"
         f"Low: {low_price}\n"
         f"Diff: {difference_price_str} || {difference_percent_str}%\n\n"
         )
   
   list_headlines = extract_headlines(news_response_dict)
   news_total_results = news_response_dict["totalResults"]
   
   print(f"Headlines for {stock_symbol}:\n"
         f"Total Results: {news_total_results}\n")
   print_headlines(list_headlines)
   
    
# Main
if __name__ == "__main__":
    main()
    