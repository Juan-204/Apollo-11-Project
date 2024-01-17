#este es un ejemplo de cambio
#ejemplo 2 para cambios
# prueba_1 para cambios en el código principal
# prueba_2 para cambios en el código principal
# prueba_3 juanjose para cambios en el codigo principal



# prueba completa de rama


# Importación del módulo logging, que proporciona funcionalidades de registro para mostrar mensajes informativos,
# de advertencia o de error durante la ejecución del script. Ayuda a rastrear la actividad del programa.
import logging

# Importación del módulo os, que ofrece funciones para interactuar con el sistema operativo, en este caso, para crear carpetas.
import os

# Importación del módulo random, que permite generar valores aleatorios. Se utiliza para asignar aleatoriamente missions y number_filess.
import random

# Importación de las clases datetime y timedelta desde el módulo datetime.
# Esto se hace para trabajar con fechas y tiempos, en este caso, para obtener la fecha actual.
from datetime import datetime, timedelta

# Importación del módulo time, que proporciona funciones relacionadas con el tiempo.
# Se utiliza específicamente la función sleep para introducir pausas en la ejecución del script, en este caso, para esperar 2 minutos.
import time

# juanjo 

def generate_file_names():
    missions = ["OrbitOne", "ColonyMoon", "VacMars", "GalaxyTwo"]
    idd = random.choice(missions)
    number_files = random.randint(1, 1000)
    return f"APL{idd}-0000{number_files}.log"

def generate_content_files(idd):
    states = ["excellent", "good", "warning", "faulty", "killed", "unknown"]
    current_date = datetime.now().strftime("%d%m%y%H%M%S")
    device_status = random.choice(states)
    content = f"""Fecha: {current_date} 
                IDD: {idd}
                Estado del dispositivo: {device_status}"""
    return content

def Synchronization():
    folder_name = "devices"
    try:
        os.mkdir(folder_name)
        logging.info("Carpeta {} creada con éxito".format(folder_name))
    except FileExistsError:
        logging.warning("La carpeta {} ya existe".format(folder_name))
    except Exception as e:
        logging.warning("Error al crear la carpeta: {}".format(e))
        
def generate():
    folder_name = "devices"
    current_date = datetime.now().strftime("%d%m%y%H%M%S")
    subfolder_name = os.path.join(folder_name, current_date)
    os.mkdir(subfolder_name)
    # Generar entre 1 y 10 archivos cada 2 minutos
    file_to_generate = random.randint(1, 10)
    for _ in range(file_to_generate):
        file_name = generate_file_names()
        path_file = os.path.join(subfolder_name, file_name)

        try:
            with open(path_file, 'w') as archive:
                content = generate_content_files(file_name.split('-')[0])
                archive.write(content)
            logging.info("Archivo {} creado con éxito".format(file_name))
        except Exception as e:
            logging.warning("Error al crear el archivo {}: {}".format(file_name, e))



# Se define una clase llamada apl_main, que encapsula el método principal del programa.
class apl_main():
    # El decorador @staticmethod indica que este método puede ser llamado en la clase sin crear una instancia de la misma.
    @staticmethod
    def main():
        Synchronization()
        # Se inicia un bucle infinito que se ejecutará continuamente.
        while True:
            # Se llama a la función Synchronization(), que crea la carpeta "devices" y genera archivos según los requisitos.
            
            generate()

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
