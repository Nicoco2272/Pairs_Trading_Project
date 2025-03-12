import matplotlib.pyplot as plt


def plot_valor_portafolio(df_backtesting):

    plt.figure(figsize=(12, 6))
    plt.plot(df_backtesting.index, df_backtesting["Valor Portafolio"], label="Valor del Portafolio", color="blue")
    plt.xlabel("Fecha")
    plt.ylabel("Valor del Portafolio")
    plt.title("Evolución del Valor del Portafolio en el Tiempo")
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    plt.show()
