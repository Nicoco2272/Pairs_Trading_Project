from Descarga_activos import descargar_datos, graficar_datos
from Prueba_DickeyFuller import prueba_estacionaridad

data = descargar_datos()
graficar_datos(data)

prueba_estacionaridad(data["V"], "Visa")
prueba_estacionaridad(data["MA"], "Mastercard")