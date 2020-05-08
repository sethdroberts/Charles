#Build a web scraper in here and verify that it works before adding it to main function

class Scavenger:
    pass

#Assemble tickers
a = 0
while a < len(SECURITY):
    TICKERS = TICKERS + CHANNEL + '.' + SECURITY[a]
    if a == len(SECURITY) - 1:
        a = a + 1
    else:
        TICKERS = TICKERS + ','
        a = a + 1
#Build a function that scrapes the web that can be imported and called by darwin