from Descarga_activos import descargar_datos, graficar_datos
from Prueba_DickeyFuller import prueba_estacionaridad
from Prueba_EngleGranger import regresion_ols, prueba_estacionaridad_residuos
from Prueba_Johanssen import prueba_johansen

def main():
    data = descargar_datos()

    prueba_estacionaridad(data["V"], "Visa")
    prueba_estacionaridad(data["MA"], "Mastercard")

    residuales = regresion_ols(data)

    prueba_estacionaridad_residuos(residuales)

    prueba_johansen(data)

    graficar_datos(data)

if __name__ == "__main__":
    main()
