import re
import collections

ticker_pattern = re.compile(r'\b[A-Z]{2,4}\b')
ticker_counter = collections.Counter()

with open("posts.txt", "r", encoding="utf-8") as file:
    for line in file:
        tickers = ticker_pattern.findall(line)
        ticker_counter.update(tickers)

print(tickers)
print(ticker_counter)

