from datetime import datetime
import pytz

# Obtén la fecha y hora actual en UTC
ahora = datetime.now(pytz.utc)

# Formatea la fecha y hora como una cadena de texto en el formato deseado
fecha_str = ahora.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

print(fecha_str)
