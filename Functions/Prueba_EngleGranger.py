from statsmodels.tsa.stattools import coint
from Descarga_activos import descargar_datos

data = descargar_datos()

def prueba_cointegracion(data):

    score, p_value, _ = coint(data["V"], data["MA"])
    print(f"Prueba de Cointegración:")
    print(f"  - Estadístico: {score:.4f}")
    print(f"  - p-valor: {p_value:.4f}")
