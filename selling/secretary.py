import numpy as np
import matplotlib.pyplot as plt

def secretary_asset_selling(prices, r=0.37):
    """ Apply the secretary strategy to decide the optimal stopping time to sell. """
    n = len(prices) - 1  # number of decision points (exclude initial point)
    observe_period = int(np.ceil(r * n))
    observed_max = np.max(prices[1:observe_period+1])

    for t in range(observe_period+1, n+1):
        if prices[t] > observed_max:
            return t, observed_max

    return n, observed_max

def simulate_gbm(S0, mu, sigma, T, n):
    """ Simulate a geometric Brownian motion price path. """
    dt = T / n
    times = np.linspace(0, T, n+1)
    prices = np.zeros(n+1)
    prices[0] = S0
    
    for t in range(1, n+1):
        z = np.random.normal()
        prices[t] = prices[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    return times, prices

def simulate_strategy(num_simulations=1000, S0=100, mu=0.05, sigma=0.2, T=1, n=100, r=0.37):
    """ Simulate the secretary asset selling strategy multiple times and compute average outcomes. """
    stopping_prices = []
    stop_times = []
    all_paths = []
    
    for i in range(num_simulations):
        times, prices = simulate_gbm(S0, mu, sigma, T, n)
        stop_index, obs_max = secretary_asset_selling(prices, r)
        stopping_prices.append(prices[stop_index])
        stop_times.append(times[stop_index])
        all_paths.append(prices)
    
    avg_price = np.mean(stopping_prices)
    avg_time = np.mean(stop_times)
    
    results = {
        "stopping_prices": stopping_prices,
        "stop_times": stop_times,
        "average_selling_price": avg_price,
        "average_stop_time": avg_time,
        "all_paths": all_paths,
        "times": times  # same time grid for all paths
    }
    return results
  
if __name__ == "__main__":
  # Parameters
  num_simulations = 1000
  S0 = 100       # initial price
  mu = 0.05      # annual drift
  sigma = 0.2    # annual volatility
  T = 1          # 1 year
  n = 100        # number of time steps
  r = 0.37       # observation period (37%)
  
  # Run simulations
  results = simulate_strategy(num_simulations, S0, mu, sigma, T, n, r)
  
  # Print summary statistics
  print(f"Average selling price: {results['average_selling_price']:.2f}")
  print(f"Average selling time: {results['average_stop_time']:.2f} (in years)")
  
  # Plot a sample of simulated paths and mark the stopping point for one example
  sample_index = 0  # you can change this to view different paths
  sample_prices = results['all_paths'][sample_index]
  sample_times = results['times']
  
  # Determine stopping index for the sample path
  stop_index, _ = secretary_asset_selling(sample_prices, r)
  
  plt.figure(figsize=(10, 6))
  plt.plot(sample_times, sample_prices, label='Asset Price')
  plt.axvline(x=sample_times[stop_index], color='red', linestyle='--', label='Stop Time')
  plt.scatter(sample_times[stop_index], sample_prices[stop_index], color='red', zorder=5)
  plt.title("Sample Price Path with Secretary Strategy Stopping Time")
  plt.xlabel("Time (years)")
  plt.ylabel("Asset Price")
  plt.legend()
  plt.grid(True)
  plt.show()
