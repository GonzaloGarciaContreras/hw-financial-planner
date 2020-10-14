# %%
"""
# Unit 5 - Financial Planning

"""

# %%
# Initial imports
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation

%matplotlib inline

# %%
# Load .env enviroment variables
load_dotenv()

# %%
"""
## Part 1 - Personal Finance Planner
"""

# %%
"""
### Collect Crypto Prices Using the `requests` Library
"""

# %%
# Set current amount of crypto assets
btc_qty = 1.2
eth_qty = 5.3

# %%
# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=CAD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=CAD"

# %%
# BTC
# Compute current value of my crpto
response_data = requests.get(btc_url).json()
#print(json.dumps(response_data, indent=4))
btc_price = response_data['data']['1']['quotes']['USD']['price']

# Compute current value of my crpto
btc_value = round((btc_qty * btc_price),2)


# %%
# ETH
## Fetch current price
response_data = requests.get(eth_url).json()
eth_price = response_data['data']['1027']['quotes']['USD']['price']

# Compute current value of my crpto
eth_value = round((eth_qty * eth_price),2)

# %%
# Print current crypto wallet balance
print(f"The current value of your {btc_price} BTC is ${btc_value:0.2f}")
print(f"The current value of your {eth_price} ETH is ${eth_value:0.2f}")

# %%
"""
### Collect Investments Data Using Alpaca: `SPY` (stocks) and `AGG` (bonds)
"""

# %%
# Current amount of stocks and bonds 
spy_qty = 50
agg_qty = 200 

# %%
# Set Alpaca API key and secret
alpaca_api_key = os.getenv("GGC_ALPACA_API_KEY")
alpaca_secret_key = os.getenv("GGC_ALPACA_SECRET_KEY")

# Create the Alpaca API object
alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version="v2"
)

# %%
# Format current date as ISO format
start_date = pd.Timestamp("2020-10-09", tz="America/New_York").isoformat()
#start_date = pd.Timestamp.today(tz="America/New_York").isoformat()[0:10]    #[0:10] only date

end_date = pd.Timestamp("2020-10-09", tz="America/New_York").isoformat()
#end_date = pd.Timestamp.today(tz="America/New_York").isoformat()[0:10]      #[0:10] only date


# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' 
timeframe = "1D"

# Get current closing prices for SPY and AGG
df_tickers = alpaca.get_barset(
    tickers,
    timeframe,
    start=start_date,
    end=end_date
).df

# Preview DataFrame
df_tickers.head()


# %%
# Pick AGG and SPY close prices
agg_close_price = df_tickers['AGG']['close'][0]
spy_close_price = df_tickers['SPY']['close'][0]


# Print AGG and SPY close prices
print(f"Current AGG closing price: ${agg_close_price}")
print(f"Current SPY closing price: ${spy_close_price}")

# %%
# Compute the current value of shares
spy_value = round((spy_qty * spy_close_price),2)
agg_value = round((agg_qty * agg_close_price),2)

# Print current value of share
print(f"The current value of your {spy_qty} SPY shares is ${spy_value:0.2f}")
print(f"The current value of your {agg_qty} AGG shares is ${agg_value:0.2f}")

# %%
"""
### Savings Health Analysis
"""

# %%
# Set monthly household income
monthly_income = 12000 

# Create savings DataFrame
savings = {'amount': [(btc_value + eth_value), (spy_value + agg_value)]}
df_savings = pd.DataFrame(savings, columns = ['amount'], index=['crypto','shares'])

# Display savings DataFrame
display(df_savings)

# %%
df_savings.plot.pie(y='amount', figsize=(5,5), title='Composition of Personal Savings')

# %%
# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
total_savings = float(df_savings.sum())

# Validate saving health
saving_healt = [
    f'Congratulations! Your savings ${total_savings} are greater than your emergency fund ${emergency_fund}',
    f'Congratulations! for reaching your goal. Savings ${total_savings} = emergency fund ${emergency_fund}',
    f'Your are ${emergency_fund - total_savings} away from reaching the goal'
    ]

if total_savings > emergency_fund: display (saving_healt[0])
elif total_savings == emergency_fund: display (saving_healt[1])
else: display (saving_healt[2])


# %%
"""
## Part 2 - Retirement Planning

### Monte Carlo Simulation
"""

# %%
# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen
start_date = pd.Timestamp('2015-08-07', tz='America/New_York').isoformat()
end_date = pd.Timestamp('2020-08-07', tz='America/New_York').isoformat()

# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' 
timeframe = "1D"

# Get current closing prices for SPY and AGG
df_tickers = alpaca.get_barset(
    tickers,
    timeframe,
    start=start_date,
    end=end_date
).df

# Preview DataFrame
df_tickers.head()

# %%
"""
1. Use the Alpaca API to fetch five years historical closing prices for a traditional `40/60` portfolio using the `SPY` and `AGG` tickers to represent the `60%` stocks (`SPY`) and `40%` bonds (`AGG`) composition of the portfolio. Make sure to convert the API output to a DataFrame and preview the output.

2. Configure and execute a Monte Carlo Simulation of `500` runs and `30` years for the `40/60` portfolio.

3. Plot the simulation results and the probability distribution/confidence intervals.
"""

# %%
# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns

# Set number of simulations
num_sims = 500
num_years = 30

# Configure a Monte Carlo simulation to forecast 30 year daily returns
MC_simulation = MCSimulation(
    portfolio_data = df_tickers,
    weights = [.4,.6],
    num_simulation = num_sims,
    num_trading_days = 252*num_years
)

# Print the simulation input data
MC_simulation.portfolio_data.head()


# %%
# Run Monte Carlo simulations to forecast cumulative daily returns
# sanity check 
#      num.of rows = 30y * 252d = 7560 (0.. 7560)
#      num of columns = 500 number of simulations (0..499)

MC_simulation.calc_cumulative_return()

# %%
# Plot simulation outcomes
line_plot = MC_simulation.plot_simulation()


# %%
# Plot probability distribution and confidence intervals
dist_plot = MC_simulation.plot_distribution()


# %%
"""
### Retirement Analysis
"""

# %%
# Fetch summary statistics from the Monte Carlo simulation results
summary_stat = MC_simulation.summarize_cumulative_return()

# Print summary statistics
print(summary_stat)


# %%
"""
### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a `$20,000` initial investment.
"""

# %%
# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
summary_stat_ci_lower = round(summary_stat[8]*initial_investment,2)
summary_stat_ci_upper = round(summary_stat[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${summary_stat_ci_lower} and ${summary_stat_ci_upper}")


# %%
"""
### Calculate the expected portfolio return at the `95%` lower and upper confidence intervals based on a `50%` increase in the initial investment.
"""

# %%
# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
summary_stat_ci_lower = round(summary_stat[8]*initial_investment,2)
summary_stat_ci_upper = round(summary_stat[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${summary_stat_ci_lower} and ${summary_stat_ci_upper}")


# %%
"""
## Optional Challenge - Early Retirement


### Five Years Retirement Option
"""

# %%
# Configuring a Monte Carlo simulation to forecast 5 years cumulative returns
# The objective is to reduce the # of years from 30 to 5 
# And increase profitability -> Higher initial investment + Higher risk weight  bonds vs stocks 

# Set number of simulations
num_sims = 500
num_years = 5

# Configure a Monte Carlo simulation to forecast 5 year daily returns 
MC_simulation = MCSimulation(
    portfolio_data = df_tickers,
    weights = [.40,.60],                            
    num_simulation = num_sims,
    num_trading_days = 252*num_years
)

# Print the simulation input data
MC_simulation.portfolio_data.head()

# %%
# Run Monte Carlo simulations to forecast cumulative daily returns
# sanity check 
#      num.of rows = 5y * 252d = 1260 
#      num of columns = 500 number of simulations (0..499)

MC_simulation.calc_cumulative_return()

# %%
# Plot simulation outcomes
line_plot = MC_simulation.plot_simulation()

# %%
# Plot probability distribution and confidence intervals
dist_plot = MC_simulation.plot_distribution()

# %%
# Fetch summary statistics from the Monte Carlo simulation results
summary_stat = MC_simulation.summarize_cumulative_return()

# Print summary statistics
print(summary_stat)

# %%
# Set initial investment
initial_investment = 60000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60k
summary_stat_ci_lower = round(summary_stat[8]*initial_investment,2)
summary_stat_ci_upper = round(summary_stat[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next {num_years} years will end within in the range of"
      f" ${summary_stat_ci_lower} and ${summary_stat_ci_upper}")

# %%
"""
### Ten Years Retirement Option
"""

# %%
# Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
# The objective is to reduce the # of years from 30 to 10 
# And increase profitability -> Higher initial investment + Higher risk weight  .25 bonds vs .75 stocks 

# Set number of simulations
num_sims = 500
num_years = 10

# Configure a Monte Carlo simulation to forecast 5 year daily returns 
MC_simulation = MCSimulation(
    portfolio_data = df_tickers,
    weights = [.25,.75],                            
    num_simulation = num_sims,
    num_trading_days = 252*num_years 
)

# Print the simulation input data
MC_simulation.portfolio_data.head()

# %%
# Run Monte Carlo simulations to forecast cumulative daily returns
# sanity check 
#      num.of rows = 10y * 252d = 2520 
#      num of columns = 500 number of simulations (0..499)

MC_simulation.calc_cumulative_return()

# %%
# Plot simulation outcomes
line_plot = MC_simulation.plot_simulation()

# %%
# Plot probability distribution and confidence intervals
dist_plot = MC_simulation.plot_distribution()

# %%
# Fetch summary statistics from the Monte Carlo simulation results
summary_stat = MC_simulation.summarize_cumulative_return()

# Print summary statistics
print(summary_stat)

# %%
# Set initial investment
initial_investment = 75000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60k
summary_stat_ci_lower = round(summary_stat[8]*initial_investment,2)
summary_stat_ci_upper = round(summary_stat[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio (weights -> bonds = {MC_simulation.weights[0]}, stocks = {MC_simulation.weights[1]}), "
      f" over the next {num_years} years will end within the range of"
      f" ${summary_stat_ci_lower} and ${summary_stat_ci_upper}")

if summary_stat_ci_lower < initial_investment:
    print(f"This is a riskier investment and it might end up in generating losses."
    f" Investment = ${initial_investment}, low-end = ${summary_stat_ci_lower}")

# %%
