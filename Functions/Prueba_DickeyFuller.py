from statsmodels.tsa.stattools import adfuller
from Descarga_activos import descargar_datos

data = descargar_datos()

def prueba_estacionaridad(series, name):
    result = adfuller(series)
    print(f"Prueba ADF para {name}:")
    print(f"  - Estadístico ADF: {result[0]:.4f}")
    print(f"  - p-valor: {result[1]:.4f}")
    print(f"  - Umbrales críticos: {result[4]} \n")

prueba_estacionaridad(data["V"], "Visa")
prueba_estacionaridad(data["MA"], "Mastercard")