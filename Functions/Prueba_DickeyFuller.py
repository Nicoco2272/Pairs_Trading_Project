from statsmodels.tsa.stattools import adfuller
from Descarga_activos import descargar_datos

def prueba_estacionaridad(series, name):
    result = adfuller(series)

    print(f"Prueba ADF para {name}:")
    print(f"  - Estadístico ADF: {result[0]:.4f}")
    print(f"  - p-valor: {result[1]:.4f}")
    print(f"  - Umbrales críticos: {result[4]} \n")

    if result[1] < 0.05:
        print(f"P-value es menor a 0.05 por lo que La serie {name} es estacionaria.")
        return False
    else:
        print(f"P-value es mayor a 0.05 por lo que la serie {name} NO es estacionaria.")
        return True

if __name__ == "__main__":
    data = descargar_datos()
    visa_estacionaria = prueba_estacionaridad(data["V"], "Visa")
    mastercard_estacionaria = prueba_estacionaridad(data["MA"], "Mastercard")

    if visa_estacionaria and mastercard_estacionaria:
        print("Ambas series no son estacionarias. Son aptas para una estrategia de pairs trading.")
    else:
        print("Al menos una serie es estacionaria. No se recomienda usar estas series para pairs trading.")
