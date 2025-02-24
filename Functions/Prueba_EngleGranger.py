import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
from Descarga_activos import descargar_datos

def regresion_ols(data):
    X = data["MA"]
    y = data["V"]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    print(model.summary())
    return model.resid

def prueba_estacionaridad_residuos(residuales):
    result = ts.adfuller(residuales)

    print("Prueba de Estacionariedad (ADF) sobre los residuos")
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"P-value: {result[1]:.4f}")
    print(f"Critical vals: {result[4]} \n")

    if result[1] < 0.05:
        print("P-value es menor a 0.05 por lo que los residuos son estacionarios y se CONFIRMA la relación de cointegración.")
    else:
        print("P-value es mayor a 0.05 por lo que los residuos NO son estacionarios entonces NO hay cointegración.")

if __name__ == "__main__":
    data = descargar_datos()
    residuales = regresion_ols(data)
    prueba_estacionaridad_residuos(residuales)



