import time
import datetime
import requests
from datetime import datetime

API_KEY = "*****INSERT API KEY*****"

#fill in all the dates that you would like to collect and should apply to all options
UNDERLYING = "QQQ"
STRIKE = 381.0
YEAR = "2021"
MONTH = "09"
DAY = "08"
DAYS_TO_EXP = "1"
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

    print(pointer)
    
    data = {"bidPrice":0,"bidSize":0,"askPrice":0,"askSize":0,"totalVolume":0,"volatility": 0,
            "delta": 0,"gamma": 0,"theta": 0,"vega": 0,"rho": 0,"markPrice":0}
    #update all the data that we want to collect and return in the form of a dict
    data["askPrice"] = pointer["ask"] 
    data["askSize"] = pointer["askSize"] 
    data["bidPrice"] = pointer["bid"] 
    data["bidSize"] = pointer["bidSize"]
    data["totalVolume"] = pointer["totalVolume"]
    data["volatility"] = pointer["volatility"]
    data["delta"] = pointer["delta"]
    data["gamma"] = pointer["gamma"]
    data["theta"] = pointer["theta"]
    data["vega"] = pointer["vega"]
    data["rho"] = pointer["rho"]
    data["markPrice"] = pointer["mark"]
    
    return data

def write_data_to_file(file_name,data_array):
    #Will write 'data_array' to desired folder 
    data_line_to_write = "\n"
    data = ",".join(data_array)
    data_line_to_write += data
    
    with open(file_name,"a") as file_data:
        file_data.write(data_line_to_write)

    file_data.close()



now = datetime.now()

current_time_long = now.strftime("%H:%M:%S")
current_time = current_time_long[0:5]


#Do not start saving data unless the market is open
while current_time != "09:30":
  print ("Pre-market --> {}".format(current_time_long))
  time.sleep(10)

  now = datetime.now()
  current_time_long = now.strftime("%H:%M:%S")
  current_time = current_time_long[0:5]

#Run and save data while the market is open
while current_time != "16:00":
  updated_information = collect_option_data(UNDERLYING,STRIKE)
  data_to_write = [current_time_long]
  for current_datapoint in updated_information:
    data_to_write.append(str(updated_information[current_datapoint]))
  write_data_to_file("MARKET_DATA.csv",data_to_write)
  print ("Updated and wrote to file at: {}".format(current_time_long))

  now = datetime.now()
  current_time_long = now.strftime("%H:%M:%S")
  current_time = current_time_long[0:5]

  time.sleep(2)

print ('DONE')