import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

def descargar_datos():
    tickers = ["V", "MA"]
    data = yf.download(tickers, start="2015-01-01", end="2025-02-20")["Close"]
    return data

def graficar_datos(data):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(data.index, data["V"], "blue", label="Visa")
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Precio Visa")
    ax1.tick_params(axis='y')

    ax1.xaxis.set_major_locator(mdates.YearLocator(1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax2 = ax1.twinx()
    ax2.plot(data.index, data["MA"], "orange", label="Mastercard")
    ax2.set_ylabel("Precio Mastercard")
    ax2.tick_params(axis='y')

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    plt.title("Precios de Visa y Mastercard")
    plt.show()

if __name__ == "__main__":
    data = descargar_datos()
    graficar_datos(data)
