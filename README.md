##Charles##

Charles is a trading bot. It is named after Charles Darwin, the originator of the theory of evolution, because it is designed to imitate the evolutionary process of "survival of the fittest." The objective of the algorithm is for all stocks in its portfolio to increase by 1%. To accomplish this, it:
    (1) finds a set of stocks that are likely to increase by >1% during the next trading day; 
    (2) if stocks increase from the market open to 1%, it liquidates the position; 
    (3) if a stock decreases below the open price, the position is liquidated and the equity moved to the stock in the portfolio which has increased the most since market open.
    (4) The portfolio is liquidated at market close.

##Getting Started##
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

#Components:
main.py -- what you run to initiate the Charles algorithm
charles_algo.py -- the primary algo file. Processes websocket data with imported functions
charles_functions.py -- 
scraper.py -- Assembles TICKER list from config file
sendsms.py -- Imports Twilio API and contains text message functionality
config.py -- Not uploaded to GitHub as it contains account details. The exact format I use is below.

#Example config.py file:
    import alpaca_trade_api as trade_api
    #Add stocks here
    SECURITIES = ['stock1', 'stock2', 'stock3', 'stock4', 'stock5', 'stock6']
    CHANNEL = 'A' #T = Trades, Q = Quotes, A = Aggregate (per second), AM = Aggregate (per minute)

    #Profit and loss bracket parameters:
    TPROFIT = 1.01
    SLOSS = .998

    #Add your Alpaca account details here:
    APCA_API_KEY_ID = 'insert-api-key'
    APCA_API_SECRET_KEY = 'insert-secret-key'
    APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
    ACCOUNT_URL = "{}/v2/acccount".format(APCA_API_BASE_URL)

    #Add Polygon account details here
    POLYGON_API_KEY = APCA_API_KEY_ID
    SOCKET = 'wss://alpaca.socket.polygon.io/stocks'

    APCA_API_KEY_ID = APCA_API_KEY_ID
    APCA_API_SECRET_KEY = APCA_API_SECRET_KEY
    APCA_API_BASE_URL = APCA_API_BASE_URL
    ACCOUNT_URL = ACCOUNT_URL

    api = trade_api.REST(APCA_API_KEY_ID,\
    APCA_API_SECRET_KEY,\
    APCA_API_BASE_URL)

    #Add Twillio details here:
    ACCOUNT_SID = 'insert-account-id-here'
    AUTH_TOKEN = 'insert-auth-token-here'
    FROM_NUM = 'insert-twilio-number'
    TO_NUM = 'insert-number-you-are-texting'

#Requirements:
python >= 3.6 (required for Polygon websocket)
alpaca_trade_api (connects to Alpaca)
websocket (for Polygon connection)
twilio (required for sending txt messages)
json (included with Python)
datetime (included with Python)
logging (included with Python)

#Installing:
Run these commands to install required libraries:
pip install alpaca_trade_api
pip install websocket-client
pip install twilio

#Deployment:
Navigate to the /Charles folder on a local or virtual machine. Run main.py in Terminal (python3 main.py).

#Built With
Alpaca API - commission-free stock brokerage
Polygon Websocket -- the stock data connection
Twilio -- API used for sending text updates to user

License
This project is licensed under the MIT License - see the LICENSE.md file for details
