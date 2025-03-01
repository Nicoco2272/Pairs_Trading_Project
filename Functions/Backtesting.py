import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

def simulate_trades(df_signal, data, initial_capital=1000000, commission=0.00125):
    capital = initial_capital
    positions = 0
    equity_curve = []
    capital_history = []

    for i in range(len(df_signal)):
        signal = df_signal["Señales"].iloc[i]
        price = data.mean(axis=1).iloc[i]

        if signal == 1:  # Señal de LONG
            shares = capital / price
            capital -= shares * price * (1 + commission)
            positions += shares
        elif signal == -1:  # Señal de SHORT
            capital += positions * price * (1 - commission)
            positions = 0  # Se cierra la posición

        total_value = capital + positions * price
        equity_curve.append(total_value)
        capital_history.append(capital)

    return pd.Series(equity_curve, index=data.index)


def calculate_performance_metrics(equity_curve):
    returns = equity_curve.pct_change().dropna()
    sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
    sortino_ratio = returns.mean() / returns[returns < 0].std() * np.sqrt(252)
    max_drawdown = (equity_curve / equity_curve.cummax() - 1).min()

    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Sortino Ratio: {sortino_ratio:.4f}")
    print(f"Max Drawdown: {max_drawdown:.4%}")
    return sharpe_ratio, sortino_ratio, max_drawdown


def plot_equity_curve(equity_curve):

    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, label="Equity Curve", color="blue")
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.xlabel("Fecha")
    plt.ylabel("Capital")
    plt.title("Evolución del Capital con el Tiempo")
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    plt.show()
