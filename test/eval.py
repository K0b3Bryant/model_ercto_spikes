import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

def calculate_metrics(returns, risk_free_rate=0.0):
    """ Calculates performance metrics. """
    total_return = (returns + 1).prod() - 1
    sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)
    downside_returns = returns[returns < 0]
    sortino_ratio = (returns.mean() - risk_free_rate) / downside_returns.std() * np.sqrt(252)
    
    return {
        "Total Return": total_return,
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
    }

def compare_to_benchmark(strategy_returns, benchmark_returns, risk_free_rate=0.0):
    """ Compares to a benchmark. """
    strategy_metrics = calculate_metrics(strategy_returns, risk_free_rate)
    benchmark_metrics = calculate_metrics(benchmark_returns, risk_free_rate)

    comparison = pd.DataFrame({
        "Metric": strategy_metrics.keys(),
        "Strategy": strategy_metrics.values(),
        "Benchmark": benchmark_metrics.values(),
    })

    return comparison

def factor_analysis(returns, factors, risk_free_rate=0.0):
    """ Performs factor analysis. """
    excess_returns = returns - risk_free_rate
    X = sm.add_constant(factors)
    model = sm.OLS(excess_returns, X).fit()

    return {
        "Alpha": model.params["const"] * 252,  # Annualized alpha
        "Alpha p-value": model.pvalues["const"],
        "Coefficients": model.params.drop("const"),
        "P-values": model.pvalues.drop("const"),
    }

def plot_cumulative_returns(strategy_returns, benchmark_returns=None, title="Cumulative Returns"):
    """Plots cumulative returns. """

    strategy_cum_returns = (strategy_returns + 1).cumprod() - 1
    plt.plot(strategy_cum_returns, label="Strategy")

    if benchmark_returns is not None:
        benchmark_cum_returns = (benchmark_returns + 1).cumprod() - 1
        plt.plot(benchmark_cum_returns, label="Benchmark", linestyle="--")

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_factor_exposures(factor_analysis_result, title="Factor Exposures"):
    """ Plots factor exposures. """
    coefficients = factor_analysis_result["Coefficients"]
    coefficients.plot(kind="bar")
    plt.title(title)
    plt.xlabel("Factors")
    plt.ylabel("Exposure")
    plt.grid(True)
    plt.show()

def main(strategy_returns, benchmark_returns, factors=None, risk_free_rate=0.0):
    """ Generates a performance report. """

    report = {}

    # Compare to Benchmark
    report["Comparison"] = compare_to_benchmark(strategy_returns, benchmark_returns, risk_free_rate)

    # Factor Analysis
    if factors is not None:
        report["Factor Analysis"] = factor_analysis(strategy_returns, factors, risk_free_rate)

    # Visualizations
    print("Plotting cumulative returns...")
    plot_cumulative_returns(strategy_returns, benchmark_returns)

    if factors is not None:
        print("Plotting factor exposures...")
        plot_factor_exposures(report["Factor Analysis"])

    return report

if __name__ == '__main__':
  report = main(strategy_returns, benchmark_returns, factors, risk_free_rate=0.0)
