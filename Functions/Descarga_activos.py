import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

def descargar_datos(tickers):
    data = yf.download(tickers, start="2015-01-01", end="2025-01-20")["Close"]
    data = data[tickers]
    return data

def graficar_datos(data, tickers):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(data.index, data[tickers[0]], "blue", label=tickers[0])
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel(f"Precio {tickers[0]}")
    ax1.tick_params(axis='y')

    ax1.xaxis.set_major_locator(mdates.YearLocator(1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax2 = ax1.twinx()
    ax2.plot(data.index, data[tickers[1]], "orange", label=tickers[1])
    ax2.set_ylabel(f"Precio {tickers[1]}")
    ax2.tick_params(axis='y')

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    plt.title(f"Precios de {tickers[0]} y {tickers[1]}")
    plt.show()

