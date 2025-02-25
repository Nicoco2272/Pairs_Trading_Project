from statsmodels.tsa.stattools import adfuller

def prueba_estacionaridad(series, name):
    result = adfuller(series)

    print(f"\n Prueba ADF para {name}:")
    print(f"  - Estadístico ADF: {result[0]:.4f}")
    print(f"  - p-valor: {result[1]:.4f}")
    print(f"  - Umbrales críticos: {result[4]} \n")

    if result[1] < 0.05:
        print(f"P-value es menor a 0.05, por lo que la serie {name} es estacionaria.\n")
        return False
    else:
        print(f"P-value es mayor a 0.05, por lo que la serie {name} NO es estacionaria.\n")
        return True

def verificar_estacionaridad_pares(data):
    tickers = data.columns.tolist()

    print(f"Orden de las columnas: {tickers}")

    if len(tickers) != 2:
        raise ValueError("Para hacer Pair-Trading asegurate de solo tener dos activos listados")

    ticker1, ticker2 = tickers

    prueba_activo1 = prueba_estacionaridad(data[ticker1], ticker1)
    prueba_activo2 = prueba_estacionaridad(data[ticker2], ticker2)

    if prueba_activo1 and prueba_activo2:
        print("Ambas series no son estacionarias. Son aptas para una estrategia de pairs trading.\n")
    else:
        print("Al menos una serie es estacionaria. No se recomienda usar estas series para pairs trading.\n")

    return prueba_activo1, prueba_activo2


