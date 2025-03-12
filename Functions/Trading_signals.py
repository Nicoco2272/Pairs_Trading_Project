import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

def trading_signals (spread_norm, data, tickers):

    umbral = 1.5

    signals = np.zeros(len(spread_norm))

    signals[spread_norm > umbral] = -1 # Short cuando el spread supera +1.5
    signals[spread_norm < umbral] = 1 # Long cuando el spread cae por debajo de -1.5
    signals[(spread_norm < umbral) & (spread_norm > -umbral)] = 0 # Cierre de posición

    df_signal = data.copy()
    df_signal["Señales"] = signals

    return df_signal



def spread_signals(spread_norm, df_signal):

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(spread_norm, label = "Spread Normalizado", color = "blue")
    ax.axhline(y = 1.5, color = "orange", linestyle = "-", linewidth= 1, label = "1.5 sigma")
    ax.axhline(y = -1.5, color = "orange", linestyle="-", linewidth = 1)

    ax.scatter(df_signal.index[df_signal["Señales"] == 1], spread_norm[df_signal["Señales"] == 1],
               color = "green", marker = "^", label = "Long", alpha = 1, s=80)
    ax.scatter(df_signal.index[df_signal["Señales"] == -1], spread_norm[df_signal["Señales"] == -1],
               color = "red", marker = "v", label = "Short", alpha = 1, s=80)

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.set_xlabel("Fecha")
    ax.set_ylabel("Spread Normalizado")
    ax.set_title("Spread Normalizado con Señales de Trading")
    ax.legend()
    ax.grid(True, linestyle="--", linewidth = 0.6, alpha = 0.7)
    plt.show()

def prices_signals(data, df_signal, tickers):

    fig, ax = plt.subplots(figsize = (12,6))



    ax.plot(data.index, data[tickers[0]], label=tickers[0], color="blue")
    ax.plot(data.index, data[tickers[1]], label=tickers[1], color="orange")

    ax.scatter(df_signal.index[df_signal["Señales"] == 1],
               data[tickers[0]][df_signal["Señales"] == 1],
               color= "green", marker = "^", label = f"Long {tickers[0]}", alpha = 1, s= 80)

    ax.scatter(df_signal.index[df_signal["Señales"] == 1],
               data[tickers[1]][df_signal["Señales"] == 1],
               color="red", marker="v", label=f"Short {tickers[1]}", alpha=1, s=80)

    ax.scatter(df_signal.index[df_signal["Señales"] == -1],
               data[tickers[0]][df_signal["Señales"] == -1],
               color="red", marker="v", label=f"Short {tickers[0]}", alpha=1, s=80)

    ax.scatter(df_signal.index[df_signal["Señales"] == -1],
               data[tickers[1]][df_signal["Señales"] == -1],
               color="green", marker="^", label=f"Long {tickers[1]}", alpha=1, s=80)

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio")
    ax.set_title(f"Precios de {tickers[0]} y {tickers[1]} con Señales de Trading")
    ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    plt.show()