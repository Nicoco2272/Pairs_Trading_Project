import pandas as pd

def ejecutar_backtesting(df_trades, tickers, spread_norm, hedge_ratios, capital_inicial=1_000_000, comision=0.00125,
                         monto_trade=10_000, capital_minimo=250_000):
    """
    Ejecuta el backtesting de la estrategia evaluando fila por fila con estructuras condicionales y verificando disponibilidad de capital.
    """
    df_backtesting = df_trades.copy()
    df_backtesting["Capital Actual"] = capital_inicial
    df_backtesting["Ventas Long"] = 0.0
    df_backtesting["Ventas Short"] = 0.0
    df_backtesting["Gasto Long"] = 0.0
    df_backtesting["Gasto Short"] = 0.0
    df_backtesting["Capital Short " + tickers[0]] = 0.0
    df_backtesting["Long shares " + tickers[0]] = 0
    df_backtesting["Short shares " + tickers[0]] = 0
    df_backtesting["Long shares " + tickers[1]] = 0
    df_backtesting["Short shares " + tickers[1]] = 0
    df_backtesting["Nuevo Capital"] = capital_inicial

    acciones_long_ticker0 = 0
    acciones_long_ticker1 = 0
    acciones_short_ticker0 = 0
    acciones_short_ticker1 = 0
    capital_actual = capital_inicial
    capital_short_ticker0 = 0.0

    prev_index = None

    for index, row in df_backtesting.iterrows():
        sigma = row["Sigma"]

        if prev_index is not None:
            capital_actual = df_backtesting.at[prev_index, "Nuevo Capital"]
            capital_short_ticker0 = df_backtesting.at[prev_index, "Capital Short " + tickers[0]]

        df_backtesting.at[index, "Capital Actual"] = capital_actual
        df_backtesting.at[index, "Capital Short " + tickers[0]] = capital_short_ticker0

        if sigma == "+1.5":  # Short Trade
            n_shares_ticker1 = int(monto_trade / row[tickers[1]])
            n_shares_ticker0 = int(n_shares_ticker1 / row["Hedge Ratio"])

            dinero_long = (n_shares_ticker1 * row[tickers[1]]) * (1 + comision)
            dinero_short = (n_shares_ticker0 * row[tickers[0]]) * (1 - comision)
            total_cost = dinero_long + dinero_short  # Ahora incluye también dinero_short

            if capital_actual - total_cost >= capital_minimo:
                capital_actual -= total_cost  # Se descuenta tanto dinero_long como dinero_short
                capital_short_ticker0 += dinero_short  # Se almacena el dinero recibido por el short
                acciones_long_ticker1 += n_shares_ticker1
                acciones_short_ticker0 += n_shares_ticker0
            else:
                n_shares_ticker1 = 0
                n_shares_ticker0 = 0
                dinero_long = 0
                dinero_short = 0

            df_backtesting.at[index, "Long shares UAL"] = n_shares_ticker1
            df_backtesting.at[index, "Short shares DAL"] = n_shares_ticker0
            df_backtesting.at[index, "Gasto Long"] = dinero_long
            df_backtesting.at[index, "Gasto Short"] = dinero_short

        elif sigma == "-1.5":  # Long Trade
            n_shares_ticker0 = int(monto_trade / row[tickers[0]])
            n_shares_ticker1 = int(n_shares_ticker0 / row["Hedge Ratio"])

            dinero_long = (n_shares_ticker0 * row[tickers[0]]) * (1 + comision)
            dinero_short = (n_shares_ticker1 * row[tickers[1]]) * (1 - comision)
            total_cost = dinero_long + dinero_short  # Ahora incluye también dinero_short

            if capital_actual - total_cost >= capital_minimo:
                capital_actual -= total_cost  # Se descuenta tanto dinero_long como dinero_short
                capital_short_ticker0 += dinero_short  # Se almacena el dinero recibido por el short
                acciones_long_ticker0 += n_shares_ticker0
                acciones_short_ticker1 += n_shares_ticker1
            else:
                n_shares_ticker0 = 0
                n_shares_ticker1 = 0
                dinero_long = 0
                dinero_short = 0

            df_backtesting.at[index, "Long shares DAL"] = n_shares_ticker0
            df_backtesting.at[index, "Short shares UAL"] = n_shares_ticker1
            df_backtesting.at[index, "Gasto Long"] = dinero_long
            df_backtesting.at[index, "Gasto Short"] = dinero_short

        elif sigma == "0":  # Cierre de Posiciones
            ventas_long = (((acciones_long_ticker0 * row[tickers[0]]) * (1 - comision)) +
                           ((acciones_long_ticker1 * row[tickers[1]]) * (1 - comision)))

            gasto_short = (((acciones_short_ticker0 * row[tickers[0]]) * (1 + comision)) +
                           ((acciones_short_ticker1 * row[tickers[1]]) * (1 + comision)))

            # Se usa el valor anterior de capital_short_ticker0 antes de ponerlo en 0
            capital_actual = capital_actual + ventas_long + (capital_short_ticker0 - gasto_short)

            df_backtesting.at[index, "Ventas Long"] = ventas_long
            df_backtesting.at[index, "Ventas Short"] = gasto_short
            df_backtesting.at[index, "Nuevo Capital"] = capital_actual

            # Se mantiene el valor anterior en la misma fecha y se borra en la siguiente iteración
            capital_short_ticker0 = 0.0

            acciones_long_ticker0 = 0
            acciones_long_ticker1 = 0
            acciones_short_ticker0 = 0
            acciones_short_ticker1 = 0

        df_backtesting.at[index, "Nuevo Capital"] = capital_actual
        df_backtesting.at[index, "Capital Short " + tickers[0]] = capital_short_ticker0
        prev_index = index

    # Renombrar columnas
    df_backtesting = df_backtesting.rename(columns={
        "Ventas Long": "Ventas de Long",
        "Ventas Short": "Recompra de short",
        "Gasto Long": "Transaccion Long",
        "Gasto Short": "Transaccion short",
        "Capital Short " + tickers[0]: "Dinero acumulado para recomprar short "
    })

    return df_backtesting
