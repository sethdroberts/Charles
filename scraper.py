import config as cfg

#Build a web scraper in here and verify that it works before adding it to main function
#In the meantime, use this function to assemble the tickers from config

#Assemble tickers
def assemble_tickers(ticker_list):
    TICKERS = ""
    a = 0
    while a < len(ticker_list):
        TICKERS = TICKERS + cfg.CHANNEL + '.' + ticker_list[a]
        if a == len(ticker_list) - 1:
            a = a + 1
        else:
            TICKERS = TICKERS + ','
            a = a + 1
    return TICKERS