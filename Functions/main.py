from Descarga_activos import descargar_datos, graficar_datos
from Prueba_DickeyFuller import prueba_estacionaridad
from Prueba_EngleGranger import prueba_cointegracion

data = descargar_datos()

prueba_estacionaridad(data["V"], "Visa")
prueba_estacionaridad(data["MA"], "Mastercard")

prueba_cointegracion(data)

graficar_datos(data)