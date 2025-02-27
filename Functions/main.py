from Descarga_activos import descargar_datos, graficar_datos, normalizar_datos
from Prueba_DickeyFuller import verificar_estacionaridad_pares
from Prueba_EngleGranger import regresion_ols, prueba_estacionaridad_residuos
from Prueba_Johanssen import prueba_johansen
from Kalman_filter import (calcular_hedge_ratio_kalman, plot_hedge_ratio)  # Importa las funciones del filtro de Kalman


def main():
    tickers = ["MA", "V"]

    data = descargar_datos(tickers)
    data_normalizada = normalizar_datos(data)
    graficar_datos(data_normalizada, tickers)

    verificar_estacionaridad_pares(data)

    residuales = regresion_ols(data)
    prueba_estacionaridad_residuos(residuales)

    spread, spread_norm = prueba_johansen(data)

    hedge_ratios = calcular_hedge_ratio_kalman(data)
    plot_hedge_ratio(hedge_ratios)


if __name__ == "__main__":
    main()