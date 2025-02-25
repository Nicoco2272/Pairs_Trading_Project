from Descarga_activos import descargar_datos, graficar_datos
from Prueba_DickeyFuller import verificar_estacionaridad_pares
from Prueba_EngleGranger import regresion_ols, prueba_estacionaridad_residuos
from Prueba_Johanssen import prueba_johansen

def main():

    tickers = ["V", "MA"]
    data = descargar_datos(tickers)

    verificar_estacionaridad_pares(data)

    residuales = regresion_ols(data)

    prueba_estacionaridad_residuos(residuales)

    prueba_johansen(data)

    graficar_datos(data, tickers)

if __name__ == "__main__":
    main()
