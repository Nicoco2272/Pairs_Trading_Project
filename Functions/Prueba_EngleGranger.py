from statsmodels.tsa.stattools import coint
from Descarga_activos import descargar_datos

data = descargar_datos()

def prueba_cointegracion(data):
    score, p_value, _ = coint(data["V"], data["MA"])

    print("Prueba de Cointegración:")
    print(f"  - Estadístico: {score:.4f}")
    print(f"  - p-value: {p_value:.4f}")

    if p_value < 0.05:
        print("P-value es menor a 0.05 por lo que las series están cointegradas. Se puede considerar una estrategia de pairs trading.")
    else:
        print("P-value es mayor a 0.05 por lo que las series NO están cointegradas. Es posible que no sean una buena pareja para el trading.")
