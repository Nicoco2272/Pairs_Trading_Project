import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

class KalmanFilterHedgeRatio:
    def __init__(self):
        self.x = np.array([0, 1])
        self.A = np.eye(2)
        self.Q = np.eye(2) * 0.01
        self.R = np.array([[0.001]])
        self.P = np.eye(2) * 10

    def predict(self):
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, x, y):
        C = np.array([[1, x]])
        S = C @ self.P @ C.T + self.R
        K = self.P @ C.T @ np.linalg.inv(S)
        self.x = self.x + K @ (y - C @ self.x)
        self.P = (np.eye(2) - K @ C) @ self.P
        return self.x[1]


def calcular_hedge_ratio_kalman(data):
    kalman_filter = KalmanFilterHedgeRatio()
    hedge_ratios = []

    for i in range(len(data)):
        kalman_filter.predict()
        x = data.iloc[i, 1]
        y = data.iloc[i, 0]
        hedge_ratio = kalman_filter.update(x, y)
        hedge_ratios.append(hedge_ratio)

    return pd.Series(hedge_ratios, index=data.index)


def ultimo_hedge_ratio(hedge_ratios):
    ultimo = hedge_ratios.iloc[-1]
    print(f"\nHedge Ratio Fijo (Último Valor Estimado): {ultimo:.4f}")
    return ultimo


def promedio_hedge_ratio(hedge_ratios):
        promedio = hedge_ratios.mean()
        print(f"\nHedge Ratio Fijo (Valor Promedio): {promedio:.4f}")
        return promedio


def plot_hedge_ratio(hedge_ratios):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hedge_ratios, label="Hedge Ratio (Kalman)", color="blue")


    ax.set_xlabel("Fecha")
    ax.set_ylabel("Hedge Ratio")
    ax.set_title("Hedge Ratio estimado con Filtro de Kalman")
    ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.show()
