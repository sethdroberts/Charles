##Charles##

Charles is a trading bot. It is named after Charles Darwin, the originator of the theory of evolution, because it is designed to imitate the evolutionary process of "survival of the fittest." The objective of the algorithm is for all stocks in its portfolio to increase by 1%. To accomplish this, it:
    (1) finds a set of stocks that are likely to increase by >1% during the next trading day; 
    (2) if stocks increase from the market open to 1%, it liquidates the position; 
    (3) if a stock decreases below the open price, the position is liquidated and the equity moved to the stock in the portfolio which has increased the most since market open.
    (4) The portfolio is liquidated at market close.

##Getting Started##
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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
