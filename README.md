Question: Cryptocurrency Exchange API Integration and Trading Platform Development
Your objective is to build a web-based trading platform for cryptocurrencies that integrates with a
cryptocurrency exchange API. The platform should provide real-time market data, enable users to place
buy/sell orders, and track their portfolio. Your tasks include:
- Choose a reputable cryptocurrency exchange API and familiarize yourself with its
documentation, authentication mechanisms, and available trading endpoints.
- Develop backend functionality to fetch real-time market data, handle user authentication, process
buy/sell orders, and retrieve portfolio information.
- Design and implement a responsive frontend interface that displays market data, allows users to
place orders, and shows their portfolio performance. Implement real-time updates for price
changes and order status.
- Consider security measures such as implementing two-factor authentication, protecting sensitive
user information, and handling API rate limits.

# Cryptocurrency Exchange API Integration and Trading Platform Development

In this project, I have develop a flask application using HTML and CSS that allows users to buy and sell stocks. The application will allow users to register, login, logout, get stock quotes, buy and sell stocks, view history of transactions, and see their portfolio.

### Features
Some of the features for this project are:
- User Registration
- User Login
- Two-factor authentication
- Get Cryptocurrency latest data
- Buy and sell Cryptocurrency
- Manage portfolio
- Handling API rate limits
  

### Running this project

`pip install -r requirements.txt`

Then run following command in the terminal:

`python app.py`

### API Integration

In this project, I have used API which is available at following website:
https://rapidapi.com/Coinranking/api/coinranking1

#### Attributes:
Following are the attributes that have been implemented in this project.
1. uuid: A unique identifier for the cryptocurrency.
2. symbol: The ticker symbol or abbreviation used to represent the cryptocurrency (e.g., BTC for Bitcoin, ETH for Ethereum).
3. name: The name of the cryptocurrency.
4. color: The color associated with the cryptocurrency, often used for visual representation.
5. iconUrl: The URL pointing to the icon or logo image of the cryptocurrency.
6. marketCap: The market capitalization of the cryptocurrency, which represents the total value of all its outstanding coins or tokens.
7. price: The current price of the cryptocurrency.
8. listedAt: The date and time when the cryptocurrency was listed or introduced.
9. tier: The tier or category assigned to the cryptocurrency based on its market capitalization or other criteria.
10. change: The percentage change in the cryptocurrency's price over a specific time period (e.g., 24 hours).
11. rank: The ranking or position of the cryptocurrency compared to other cryptocurrencies based on factors such as market capitalization or trading volume.
12. sparkline: A visual representation, often in the form of a line graph, showing the price movement or volatility of the cryptocurrency over a specific time period.
13. lowVolume: A flag indicating whether the cryptocurrency has low trading volume or liquidity.
14. coinrankingUrl: The URL that provides more information about the cryptocurrency on the Coinranking platform.
15. 24hVolume: The trading volume of the cryptocurrency over the last 24 hours, representing the total value of all the coins or tokens traded.
16. btcPrice: The price of the cryptocurrency denominated in Bitcoin (BTC) or its equivalent value in BTC.

### Web Application
For web application, I have used flask, a python web framework. I have used HTML and CSS for frontend. I have used SQLite database for storing user information and transactions.

### Demo




https://github.com/AnishMachamasi/Genese-Assignment/assets/98002255/042a5679-170b-40b0-b40b-7f2ec5598aec



