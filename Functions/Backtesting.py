import pandas as pd

def ejecutar_backtesting(df_trades, tickers, spread_norm, hedge_ratios, capital_inicial=1_000_000, comision=0.00125,
                         monto_trade=6_000, capital_minimo=250_000):

    df_backtesting = df_trades.copy()
    df_backtesting["Capital Actual"] = capital_inicial
    df_backtesting["Ventas Long"] = 0.0
    df_backtesting["Ventas Short"] = 0.0
    df_backtesting["Gasto Long"] = 0.0
    df_backtesting["Gasto Short"] = 0.0
    df_backtesting["Comisión Short"] = 0.0
    df_backtesting["Long shares " + tickers[0]] = 0
    df_backtesting["Short shares " + tickers[0]] = 0
    df_backtesting["Long shares " + tickers[1]] = 0
    df_backtesting["Short shares " + tickers[1]] = 0
    df_backtesting["Nuevo Capital"] = capital_inicial

    # Agregar nuevas columnas de acumulación
    df_backtesting["Long " + tickers[0] + " shares acumuladas"] = 0
    df_backtesting["Short " + tickers[0] + " shares acumuladas"] = 0
    df_backtesting["Long " + tickers[1] + " shares acumuladas"] = 0
    df_backtesting["Short " + tickers[1] + " shares acumuladas"] = 0

    # Nueva columna: Dinero acumulado para los Long
    df_backtesting["Dinero acumulado Long"] = 0.0

    # Nueva columna: Dinero acumulado para los Short
    df_backtesting["Dinero acumulado Short"] = 0.0

    # Nueva columna: Dinero en activos Long a día de hoy
    df_backtesting["Dinero en activos Long a día de hoy"] = 0.0

    # Nueva columna: Dinero en activos Short a día de hoy
    df_backtesting["Dinero en activos Short a día de hoy"] = 0.0

    # Nueva columna: Ganancia/Perdida activo short
    df_backtesting["Ganancia/Perdida activo short"] = 0.0

    # Nueva columna: Valor Portafolio
    df_backtesting["Valor Portafolio"] = 0.0

    acciones_long_ticker0 = 0
    acciones_long_ticker1 = 0
    acciones_short_ticker0 = 0
    acciones_short_ticker1 = 0
    capital_actual = capital_inicial
    capital_short_ticker0 = 0.0
    capital_long_acumulado = 0.0

    prev_index = None

    for index, row in df_backtesting.iterrows():
        sigma = row["Sigma"]

        if prev_index is not None:
            capital_actual = df_backtesting.at[prev_index, "Nuevo Capital"]
            capital_short_ticker0 = df_backtesting.at[prev_index, "Dinero acumulado Short"]
            capital_long_acumulado = df_backtesting.at[prev_index, "Dinero acumulado Long"]

        df_backtesting.at[index, "Capital Actual"] = capital_actual

        if sigma == "+1.5":  # Short Trade #Long ticker[0] y short ticker[1]
            n_shares_ticker0 = int(monto_trade / row[tickers[0]])
            n_shares_ticker1 = int(n_shares_ticker0 * row["Hedge Ratio"])

            dinero_long = (n_shares_ticker0 * row[tickers[0]]) * (1 + comision)
            dinero_short = (n_shares_ticker1 * row[tickers[1]])
            total_cost = dinero_long

            if capital_actual - total_cost >= capital_minimo:
                capital_actual -= total_cost
                capital_short_ticker0 += dinero_short
                capital_long_acumulado += dinero_long
                acciones_long_ticker0 += n_shares_ticker0
                acciones_short_ticker1 += n_shares_ticker1
            else:
                n_shares_ticker0 = 0
                n_shares_ticker1 = 0
                dinero_long = 0
                dinero_short = 0

            comision_short = dinero_short * comision
            capital_actual -= comision_short

        elif sigma == "-1.5":  # Long Trade #Short ticker[0] #Long ticker[1]
            n_shares_ticker1 = int(monto_trade / row[tickers[1]])
            n_shares_ticker0 = int(n_shares_ticker1 / row["Hedge Ratio"])

            dinero_long = (n_shares_ticker1 * row[tickers[1]]) * (1 + comision)
            dinero_short = (n_shares_ticker0 * row[tickers[0]])
            total_cost = dinero_long

            if capital_actual - total_cost >= capital_minimo:
                capital_actual -= total_cost
                capital_short_ticker0 += dinero_short
                capital_long_acumulado += dinero_long
                acciones_long_ticker1 += n_shares_ticker1
                acciones_short_ticker0 += n_shares_ticker0
            else:
                n_shares_ticker0 = 0
                n_shares_ticker1 = 0
                dinero_long = 0
                dinero_short = 0

            comision_short = dinero_short * comision
            capital_actual -= comision_short

        elif sigma == "0":  # Cierre de Posiciones
            ventas_long = (((acciones_long_ticker0 * row[tickers[0]]) * (1 - comision)) +
                           ((acciones_long_ticker1 * row[tickers[1]]) * (1 - comision)))

            gasto_short = (acciones_short_ticker0 * row[tickers[0]])  + (acciones_short_ticker1 * row[tickers[1]])

            capital_actual = capital_actual + ventas_long + (capital_short_ticker0 - (gasto_short * (1 - comision)))
            capital_short_ticker0 = 0.0
            capital_long_acumulado = 0.0
            acciones_long_ticker0 = 0
            acciones_long_ticker1 = 0
            acciones_short_ticker0 = 0
            acciones_short_ticker1 = 0

        df_backtesting.at[index, "Nuevo Capital"] = capital_actual

        # Calcular el dinero en activos Long y Short a día de hoy
        dinero_activos_long = (acciones_long_ticker0 * row[tickers[0]]) + (acciones_long_ticker1 * row[tickers[1]])
        df_backtesting.at[index, "Dinero en activos Long a día de hoy"] = dinero_activos_long

        dinero_activos_short = (acciones_short_ticker0 * row[tickers[0]]) + (acciones_short_ticker1 * row[tickers[1]])
        df_backtesting.at[index, "Dinero en activos Short a día de hoy"] = dinero_activos_short

        # Calcular la ganancia/pérdida en activo short
        ganancia_perdida_short = capital_short_ticker0 - dinero_activos_short
        df_backtesting.at[index, "Ganancia/Perdida activo short"] = ganancia_perdida_short

        # Calcular el Valor del Portafolio
        df_backtesting.at[index, "Valor Portafolio"] = (
            df_backtesting.at[index, "Nuevo Capital"] +
            df_backtesting.at[index, "Dinero en activos Long a día de hoy"] +
            df_backtesting.at[index, "Ganancia/Perdida activo short"]
        )

        # Actualizar las columnas de acumulación
        df_backtesting.at[index, "Dinero acumulado Long"] = capital_long_acumulado
        df_backtesting.at[index, "Dinero acumulado Short"] = capital_short_ticker0

        prev_index = index

    return df_backtesting
