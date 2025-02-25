from statsmodels.tsa.vector_ar.vecm import coint_johansen
from Descarga_activos import descargar_datos
import numpy as np

data = descargar_datos()

def prueba_johansen(data, det_order=-1, k_ar_diff=1):
    """
    Ejecuta el test de cointegración de Johansen.
    det_order = -1 (solo constante)
    k_ar_diff = 1 (diferencias de primer orden)
    """
    johansen_test = coint_johansen(data.values, det_order, k_ar_diff)

    print("Valores propios (Eigenvalues):", johansen_test.eig)
    print("\nEstadísticos de la traza:")
    for i in range(len(johansen_test.lr1)):
        print(f"  - r ≤ {i}: {johansen_test.lr1[i]:.4f} (valor crítico {johansen_test.cvt[i, 1]:.4f})")

    print("\nEstadísticos del máximo eigenvalor:")
    for i in range(len(johansen_test.lr2)):
        print(f"  - r = {i}: {johansen_test.lr2[i]:.4f} (valor crítico {johansen_test.cvm[i, 1]:.4f})")

    # Evaluar si hay cointegración
    r = np.where(johansen_test.lr1 > johansen_test.cvt[:, 1])[0]
    if len(r) > 0:
        print(f"\nCointegración detectada con r = {r[-1]}")
    else:
        print("\nNo se detectó cointegración.")

prueba_johansen(data)
