import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
from Descarga_activos import descargar_datos

def regresion_ols(data):
    tickers = data.columns.tolist()

    X = data[tickers[1]]
    y = data[tickers[0]]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    print(model.summary())

    hedge_ratio = model.params[tickers[1]]
    print(f"\nEl Hedge Ratio es {hedge_ratio:.4f} {tickers[1]} por 1 de {tickers[0]}\n")

    return model.resid

def prueba_estacionaridad_residuos(residuales):
    result = ts.adfuller(residuales)

    print("\nPrueba de Estacionariedad (ADF) sobre los residuos:")
    print(f"- ADF Statistic: {result[0]:.4f}")
    print(f"- P-value: {result[1]:.4f}")
    print(f"- Critical vals: {result[4]} \n")

    if result[1] < 0.05:
        print("P-value es menor a 0.05 por lo que los residuos son estacionarios y se CONFIRMA la relación de cointegración.\n ")
    else:
        print("P-value es mayor a 0.05 por lo que los residuos NO son estacionarios entonces NO hay cointegración.")




