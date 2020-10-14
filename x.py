


















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
