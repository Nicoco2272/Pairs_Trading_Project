import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

sns.set_style("darkgrid")


def generar_dataframe_trades(df_signal, tickers, spread_norm, hedge_ratios):
    df_trades = df_signal.copy()
    df_trades["Hedge Ratio"] = hedge_ratios
    df_trades["Sigma"] = "N/A"
    df_trades["Trade"] = "N/A"
    df_trades["Accion_" + tickers[0]] = "N/A"
    df_trades["Accion_" + tickers[1]] = "N/A"
    df_trades["Cerrar Posicion"] = "N/A"


    df_trades.loc[df_trades["Señales"] == 1, "Sigma"] = "-1.5"
    df_trades.loc[df_trades["Señales"] == -1, "Sigma"] = "+1.5"

    df_trades.loc[df_trades["Señales"] == 1, "Trade"] = "Long"
    df_trades.loc[df_trades["Señales"] == -1, "Trade"] = "Short"

    df_trades.loc[df_trades["Señales"] == 1, "Accion_" + tickers[0]] = "Short" #Y
    df_trades.loc[df_trades["Señales"] == 1, "Accion_" + tickers[1]] = "Long" #X
    df_trades.loc[df_trades["Señales"] == -1, "Accion_" + tickers[0]] = "Long" #Y
    df_trades.loc[df_trades["Señales"] == -1, "Accion_" + tickers[1]] = "Short" #X

    # Cerrar posiciones si el spread normalizado está cerca de 0
    df_trades.loc[abs(spread_norm) < 0.05, "Cerrar Posicion"] = "Cerrar Posiciones"
    df_trades.loc[abs(spread_norm) < 0.05, "Sigma"] = "0"

    return df_trades


def plot_prices_and_spread(data, spread_norm, df_signal, tickers, umbral=1.5):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    # Precios con señales de trading
    ax1.plot(data.index, data[tickers[0]], label=tickers[0], color="blue")
    ax1.plot(data.index, data[tickers[1]], label=tickers[1], color="orange")

    # Señales LONG y SHORT para ambos activos
    ax1.scatter(df_signal.index[df_signal["Señales"] == 1],
                data[tickers[0]][df_signal["Señales"] == 1],
                color="skyblue", marker="v", label=f"Short {tickers[0]}", alpha=1, s=80) #Y Short

    ax1.scatter(df_signal.index[df_signal["Señales"] == 1],
                data[tickers[1]][df_signal["Señales"] == 1],
                color="purple", marker="^", label=f"Long {tickers[1]}", alpha=1, s=80) #X Long

    ax1.scatter(df_signal.index[df_signal["Señales"] == -1],
                data[tickers[0]][df_signal["Señales"] == -1],
                color="green", marker="^", label=f"Long {tickers[0]}", alpha=1, s=80) #Y Long

    ax1.scatter(df_signal.index[df_signal["Señales"] == -1],
                data[tickers[1]][df_signal["Señales"] == -1],
                color="red", marker="v", label=f"Short {tickers[1]}", alpha=1, s=80) #X Short

    ax1.set_ylabel("Precio")
    ax1.set_title(f"Precios de {tickers[0]} y {tickers[1]} con Señales de Trading")
    ax1.legend()
    ax1.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)

    # Spread normalizado
    ax2.plot(spread_norm, label="Spread Normalizado", color="blue")

    ax2.axhline(y=umbral, color="orange", linestyle="-", linewidth=1, label=f"{umbral} sigma")
    ax2.axhline(y=-umbral, color="orange", linestyle="-", linewidth=1)

    ax2.set_xlabel("Fecha")
    ax2.set_ylabel("Spread Normalizado")
    ax2.legend()
    ax2.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)

    ax2.xaxis.set_major_locator(mdates.YearLocator(1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()