import re

# Archivo de entrada y salida
archivo_entrada = "datos_salidas.txt"
archivo_salida = "consultas_salidas.sql"
archivo_destinos = "mapeados.txt"  # Archivo con los destinos mapeados

# Configuración de aeropuerto de salida
aeropuerto_salida = "Badajoz LEBZ"

# Inicialización de variables
fecha_actual = None
consultas = []
destinos_mapeados = {}

# Cargar los destinos mapeados desde un archivo
with open(archivo_destinos, "r", encoding="utf-8") as f_destinos:
    for linea in f_destinos:
        # Limpiar la línea y dividir por coma
        partes = linea.strip().split(',')
        if len(partes) == 2:
            destino_original, destino_mapeado = partes
            destinos_mapeados[destino_original.strip()] = destino_mapeado.strip()

# Verificar si el diccionario de destinos se ha cargado correctamente
print(f"Destinos mapeados cargados: {destinos_mapeados}")

# Procesar el archivo de entrada
with open(archivo_entrada, "r", encoding="utf-8") as entrada:
    lineas = entrada.readlines()

for i, linea in enumerate(lineas):
    linea = linea.strip()
    
    # Si la línea es una fecha, actualizamos la fecha actual
    if re.match(r"\d{2}/\d{2}/\d{4}", linea):
        fecha_actual = linea
        continue
    
    # Si encontramos una hora, procesamos el bloque correspondiente
    if re.match(r"\d{2}:\d{2}", linea):
        try:
            # Extraer el bloque de 8 líneas
            hora = linea
            vuelo_codigo = lineas[i + 1].strip()
            aerolinea = lineas[i + 2].strip()
            destino = lineas[i + 3].strip()
            
            # Validar que el bloque contenga datos necesarios
            if not (fecha_actual and hora and vuelo_codigo and aerolinea and destino):
                print(f"Bloque incompleto en línea {i+1}. Ignorado.")
                continue
            
            # Reemplazar el destino con el mapeo adecuado si existe
            if destino in destinos_mapeados:
                destino = destinos_mapeados[destino]
            
            # Convertir la fecha al formato YYYY-MM-DD
            fecha_formateada = "-".join(reversed(fecha_actual.split("/")))
            
            # Crear consulta SQL
            consulta = f"""
INSERT INTO `vuelos` (`id`, `tipo`, `company`, `dep`, `arr`, `fecha`, `hora`, `vuelo`, `terminal`) 
VALUES (NULL, 'Salida', '{aerolinea}', '{aeropuerto_salida}', '{destino}', '{fecha_formateada}', '{hora}:00', '{vuelo_codigo}', '1');
"""
            consultas.append(consulta.strip())
        
        except IndexError:
            print(f"Error procesando bloque en la línea {i+1}.")
            continue

# Guardar consultas en el archivo de salida
with open(archivo_salida, "w", encoding="utf-8") as salida:
    salida.write("\n".join(consultas))

print(f"Procesamiento completado. {len(consultas)} consultas generadas.")