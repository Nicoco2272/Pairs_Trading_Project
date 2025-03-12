from Descarga_activos import descargar_datos, graficar_datos, normalizar_datos
from Prueba_DickeyFuller import verificar_estacionaridad_pares
from Prueba_EngleGranger import regresion_ols, prueba_estacionaridad_residuos
from Prueba_Johanssen import prueba_johansen
from Kalman_filter import (calcular_hedge_ratio_kalman, plot_hedge_ratio,ultimo_hedge_ratio,promedio_hedge_ratio, generar_dataframe_hedge_ratio)
from Trading_signals import (trading_signals, spread_signals, prices_signals)
from Backtesting import ejecutar_backtesting
from Graficos_juntos import plot_prices_and_spread, generar_dataframe_trades

def main():
    tickers = ["DAL","UAL"]

    data = descargar_datos(tickers)
    data_normalizada = normalizar_datos(data)
    graficar_datos(data, tickers)

    verificar_estacionaridad_pares(data)

    residuales = regresion_ols(data)
    prueba_estacionaridad_residuos(residuales)

    spread, spread_norm = prueba_johansen(data)

    hedge_ratios = calcular_hedge_ratio_kalman(data)
    df_hedge = generar_dataframe_hedge_ratio(data)
    print(df_hedge)
    plot_hedge_ratio(hedge_ratios)

    df_signal = trading_signals(spread_norm, data, tickers)
    spread_signals(spread_norm, df_signal)

    df_trades = generar_dataframe_trades(df_signal, tickers, spread_norm,hedge_ratios)
    print(df_trades)
    #df_trades.to_csv("trading_trades_data.csv")
    plot_prices_and_spread(data, spread_norm, df_signal, tickers)

    df_backtesting = ejecutar_backtesting(df_trades, tickers, spread_norm, hedge_ratios)
    print(df_backtesting)
    df_backtesting.to_csv("backtesting_results2.csv")

if __name__ == "__main__":
    main()