**Introduction**

This project displays creates a dashoabrd that used the current best bid and ask for an option to create a market-by-price (MBP) orderbook and depth chart. The project uses the TD Ameritrade Options Chain API (https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains) to all option data which is then saved periodically and graphed live thougout the day (9:30AM to 4:00PM). All funtionality currently included in the project is described below. 

**Order Book**

When the API is called I collect the current best bid-ask and save that to a hashmap of prices that are determined based on the openning price of the option (the option premium at market-open) This data is then graphed into a orderbook. When the nest update is made (withing the next 2 seconds) the order book is updated based on the new best bid and ask price. I assume that no orders are cancelled since I do not currenly have access to that data, meaning that if a bid comes in and the next best bid is higher I assume that the previous bid went unfilled and is still on the orderbook.

![Example Image of the Orderbook](https://github.com/JoJo10Smith/Level-II-Options-Dashboard/blob/main/Example%20Images/newplot%20(3).png)

**Depth Chart Book**

The Depth Chart is based on data from the order book but is instead cumulative meaning that for a given price, you can either see the total volume of options that would be sold/ bought at that price. Again I assume once an oder is sent, it is either filled or stays on the book and is cancelled at market-close if it is still on the orderbook. This allowed me to better place my limit orders. If there was a large bid at a price level, I would place my bid above that to ensure that my order got filled before a reletiley large number of orders came in.

![Example Image of the Depth Chart](https://github.com/JoJo10Smith/Level-II-Options-Dashboard/blob/main/Example%20Images/newplot%20(1).png)

**Mark Price and Volume Tracker**

Unfortunetely, my broker did not provide me with historical option prices unless I had the option in my portfolio, I wanted to see how option premiums were fluctuating before I bought/sold them. To do this I used the mark-price (midpoint between the besd best and ask price) and tracked that over time. Alongside the mark-price, I also tracked the volume. The TD Ameritrade API only gave me total volume at the time of the API call so I had to keep track of the previuos volume to calculate the volume between two time periods. I used this information to gather insights about the best time to sell/ buy my options. If I saw that there was a lot of volume then I knew that my orders would be filled reletively quickly. According to the information gathered (image is below) most trading happened in the morning so that was when I did most of my trading since the market had more liquidity in the morninig when compared to the afternoon. 

![Example Image of the Orderbook](https://github.com/JoJo10Smith/Level-II-Options-Dashboard/blob/main/Example%20Images/364%20call.JPG)

**Option Greek Tracker**

Lastly I decided to implement tracker for the option greeks (Delta, Gamma, Vega, Theta, and Rho). All of the option greeks were tracked live througout the day meaing that I could see the relationship between any of the greeks and the price of the underlying and vice versa to assist in my understanding of option pricing. I hope to next develop methods to estimate option premium using the saved data thougout a trading day.
