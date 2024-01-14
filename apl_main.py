# prueba_1 para cambios en el código principal
# prueba_2 para cambios en el código principal


# Importación del módulo logging, que proporciona funcionalidades de registro para mostrar mensajes informativos,
# de advertencia o de error durante la ejecución del script. Ayuda a rastrear la actividad del programa.
import logging

# Importación del módulo os, que ofrece funciones para interactuar con el sistema operativo, en este caso, para crear carpetas.
import os

# Importación del módulo random, que permite generar valores aleatorios. Se utiliza para asignar aleatoriamente misiones y etiquetas.
import random

# Importación de las clases datetime y timedelta desde el módulo datetime.
# Esto se hace para trabajar con fechas y tiempos, en este caso, para obtener la fecha actual.
from datetime import datetime, timedelta

# Importación del módulo time, que proporciona funciones relacionadas con el tiempo.
# Se utiliza específicamente la función sleep para introducir pausas en la ejecución del script, en este caso, para esperar 2 minutos.
import time

# juanjo 

def generar_nombre_archivo():
    misiones = ["OrbitOne", "ColonyMoon", "VacMars", "GalaxyTwo"]
    mision = random.choice(misiones)
    etiqueta = random.randint(1, 1000)
    return f"APL{mision}-0000{etiqueta}.log"

def generar_contenido_archivo(mision):
    estados = ["excellent", "good", "warning", "faulty", "killed", "unknown"]
    fecha_actual = datetime.now().strftime("%d%m%y%H%M%S")
    estado_dispositivo = random.choice(estados)

    contenido = f"""Fecha: {fecha_actual}
Mision: {mision}
Estado del dispositivo: {estado_dispositivo}
"""

    return contenido

def sincronizacion():
    nombre_carpeta = "devices"
    try:
        os.mkdir(nombre_carpeta)
        logging.info("Carpeta {} creada con éxito".format(nombre_carpeta))
    except FileExistsError:
        logging.warning("La carpeta {} ya existe".format(nombre_carpeta))
    except Exception as e:
        logging.warning("Error al crear la carpeta: {}".format(e))
        
def generar():
    nombre_carpeta = "devices"
    fecha_actual = datetime.now().strftime("%d%m%y%H%M%S")
    nombre_subcarpeta = os.path.join(nombre_carpeta, fecha_actual)
    os.mkdir(nombre_subcarpeta)
    # Generar entre 1 y 10 archivos cada 2 minutos
    archivos_a_generar = random.randint(1, 10)
    for _ in range(archivos_a_generar):
        nombre_archivo = generar_nombre_archivo()
        path_archivo = os.path.join(nombre_subcarpeta, nombre_archivo)

        try:
            with open(path_archivo, 'w') as archivo:
                contenido = generar_contenido_archivo(nombre_archivo.split('-')[0])
                archivo.write(contenido)
            logging.info("Archivo {} creado con éxito".format(nombre_archivo))
        except Exception as e:
            logging.warning("Error al crear el archivo {}: {}".format(nombre_archivo, e))



# Se define una clase llamada apl_main, que encapsula el método principal del programa.
class apl_main():
    # El decorador @staticmethod indica que este método puede ser llamado en la clase sin crear una instancia de la misma.
    @staticmethod
    def main():
        sincronizacion()
        # Se inicia un bucle infinito que se ejecutará continuamente.
        while True:
            # Se llama a la función sincronizacion(), que crea la carpeta "devices" y genera archivos según los requisitos.
            
            generar()

            # Se añade un comentario para explicar que se espera 2 minutos antes de la próxima generación de archivos.
            # Esto cumple con el requisito de generar archivos cada 2 minutos.
            time.sleep(20)

# La siguiente línea se asegura de que el bloque de código debajo de ella solo se ejecute si este script es ejecutado directamente.
if __name__ == "__main__":
    # Configuración del sistema de registro (logging) para mostrar mensajes de nivel INFO o superior.
    # Esto proporciona información sobre la ejecución del script, como mensajes de éxito o advertencias.
    logging.basicConfig(level=logging.INFO)

    # Se llama al método estático main() de la clase apl_main para iniciar la ejecución del programa.
    apl_main.main()
