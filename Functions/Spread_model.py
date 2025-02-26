import matplotlib.pyplot as plt
import numpy as np
from Prueba_Johanssen import prueba_johansen

def calcular_y_plotear_spread(data):
    """
    Calcula y grafica el spread basado en los coeficientes obtenidos del test de Johansen.
    """
    tickers = data.columns.tolist()

    # Obtener coeficientes del modelo de spread desde Johansen
    spread_model = prueba_johansen(data, return_spread=True)  # Ahora devolverá los coeficientes

    # Verificar si el modelo de spread se obtuvo correctamente
    if spread_model is None:
        print("No se pudo obtener el modelo de spread.")
        return

    # Calcular el spread: u_t = coef1 * x_t + coef2 * y_t
    u_t = spread_model[0] * data[tickers[0]] + spread_model[1] * data[tickers[1]]

    # Graficar el spread
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, u_t, label="Spread", color="purple")
    plt.axhline(y=np.mean(u_t), color='red', linestyle='--', label="Media del spread")
    plt.xlabel("Fecha")
    plt.ylabel("Spread")
    plt.title(f"Modelo de Spread: {tickers[0]} vs {tickers[1]}")
    plt.legend()
    plt.grid()
    plt.show()

    print(f"\nModelo de Spread: u_t = {spread_model[0]:.5f} * {tickers[0]} {spread_model[1]:+.5f} * {tickers[1]}")
