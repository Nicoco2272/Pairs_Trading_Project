import statsmodels.tsa.vector_ar.vecm as vecm
import matplotlib.pyplot as plt
import numpy as np

def prueba_johansen(data, plot_spread=True):

    X = data.dropna()
    tickers = data.columns.tolist()

    johansen_test = vecm.coint_johansen(X, det_order=0, k_ar_diff=1)

    print("\nEigenvalue Statistics:", johansen_test.lr1)
    print("Trace Statistics:", johansen_test.lr2)
    print("Eigenvalues:", johansen_test.eig)
    print("Eigenvectors:")
    print(johansen_test.evec)

    spread_model = johansen_test.evec[:, 0]
    print(f"\nNuestro modelo de spread es:\n u_t = {spread_model[0]:.5f} * {tickers[1]} {spread_model[1]:+.5f} * {tickers[0]}")

    spread = spread_model[0] * data[tickers[1]] + spread_model[1] * data[tickers[0]]

    if plot_spread:
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, spread, label="Spread", color="blue")
        plt.axhline(y=np.mean(spread), color='red', linestyle='--', label="Media del spread")
        plt.xlabel("Fecha")
        plt.ylabel("Spread")
        plt.title(f"Modelo de Spread: {tickers[0]} vs {tickers[1]}")
        plt.legend()
        plt.grid()
        plt.show()

    return spread


