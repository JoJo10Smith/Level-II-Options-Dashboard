import scipy.stats
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas 
import time

API_KEY = "***INSERT YOUR TD AMERITRADE API KEY***"

UNDERLYING = "QQQ"
YEAR = "2021"
MONTH = "09"
DAY = "20" 
DAYS_TO_EXP = "3"

OPTION_START,OPTION_END = 365,380
UNDERLYING_START,UNDERLYING_END = 360,385
UNDERLYING_PRICE = 374.36


#fill in all the dates that you would like to collect and should apply to all options
API_DATE_INPUT = "{}-{}-{}:{}".format(YEAR,MONTH,DAY,DAYS_TO_EXP)

def collect_option_data(symbol,strike,contractType="CALL"):
    #Collect all relevant information about an option that will be analyzed
    parameters = {"apikey":API_KEY,
                 "includeQuotes":True,
                 "strike":str(strike),
                 "symbol":symbol,
                 "contractType":contractType}
        
    url = "https://api.tdameritrade.com/v1/marketdata/chains"
    response = requests.get(url,params=parameters).json()
    pointer = response['callExpDateMap'][API_DATE_INPUT][str(parameters['strike'])][0]
    
    return pointer["ask"]
    
def create_option_strikes(starting_strike,ending_strike,step=1):
  #create the desired list of strike prices for the option heatmap
  list_of_strikes = []
  for current_strike in range(starting_strike,ending_strike+step,step):
    list_of_strikes.append(current_strike)
  return list_of_strikes

def create_underlying_prices(starting_price,ending_price,step=1):
  #create the desired list of prices for the heatmap
  list_of_prices = []
  for current_price in range(starting_price,ending_price+step,step):
    list_of_prices.append(current_price)
  return list_of_prices

PROFITABILITY = {}

OPTION_STRIKES = create_option_strikes(OPTION_START,OPTION_END)
UNDERLYING_PRICES = create_underlying_prices(UNDERLYING_START,UNDERLYING_END)

OPTION_PREMIUM = {}
for current_option_strike in OPTION_STRIKES:
  option_price = collect_option_data(UNDERLYING,float(current_option_strike))
  OPTION_PREMIUM[current_option_strike] = option_price
  print ("Option Premium for ${} strike --> ${}".format(float(current_option_strike),option_price))
  time.sleep(0.5)

#read the data from prepared file
file_data = [line.split(",") for line in open("QQQ_return_data.csv")]
file_data = file_data[1:]

RETURN_DATA = {}
for current_line in file_data:
  days_to_exp = str(current_line[0])
  mean_return = float(current_line[1])
  standard_dev = float(current_line[2])
  RETURN_DATA[days_to_exp] = {"mean":mean_return,"standard_dev":standard_dev}

def _required_return_(original_price,target_price):
  #calculates the return you would need to reach your target
  difference = target_price - original_price
  return float(difference/original_price)

def calculate_probability(current_live_price,underlying_calc_price):
  #calculates probablity of achiveing desired return based on pas performance
  data = RETURN_DATA[DAYS_TO_EXP]
  distribution = scipy.stats.norm(data["mean"],data["standard_dev"])
  required_return = _required_return_(current_live_price,underlying_calc_price)
  return  1 - distribution.cdf(required_return)

data = {}
for current_option_strike in OPTION_STRIKES:
    option_profits = []

    for current_underlying_price in UNDERLYING_PRICES:
        if current_option_strike >= current_underlying_price:
            current_profit = -OPTION_PREMIUM[current_option_strike]
        else:
            current_profit = current_underlying_price - current_option_strike - OPTION_PREMIUM[current_option_strike]
        
        profit_percent = 100 * float(current_profit/OPTION_PREMIUM[current_option_strike])
        #profit_percent = max(min(500,profit_percent),-100)
        profit_percent *= calculate_probability(UNDERLYING_PRICE,current_underlying_price)
        option_profits.append(min(200,profit_percent))
    data[current_option_strike] = option_profits

GRAPH_DATA = pandas.DataFrame.from_dict(data,orient = "index",columns = UNDERLYING_PRICES)

fig = px.imshow(GRAPH_DATA,color_continuous_scale="RdYlGn",title="Expected value of Option returns for {}".format(UNDERLYING))

fig.update_xaxes(title_text='Underlying Price')
fig.update_yaxes(title_text='Option Strike Price')

def add_profitabilty_lines(given_data,underlying_prices):
  x,y=[],[]
  for current_strike in given_data:
    current_index = 0
    for current_profit in given_data[current_strike]:
      if current_profit > 0:
        y.append(current_strike-0.5)
        y.append(current_strike+0.5)
        x.append(underlying_prices[current_index]-0.5)
        x.append(underlying_prices[current_index]-0.5)
        break 
      else:
        current_index += 1
  return [x,y]

line_data = add_profitabilty_lines(data,UNDERLYING_PRICES)
fig.add_trace(
    go.Scatter(
        x=line_data[0],
        y=line_data[1],
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=False))

fig.show()