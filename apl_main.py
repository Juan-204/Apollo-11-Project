import hashlib
import logging
from msilib.schema import Component

import os

import random

from datetime import datetime, timedelta

import time

def generate_content_files(idd):
    """
    Genera contenido para archivos de estado del dispositivo.
    Args idd: cadena como identificador de dispositivo
    Devuelve str: una cadena que contiene información sobre el estado del dispositivo,
    incluyendo la fecha actual, el identificador del dispositivo (IDD) y el estado del dispositivo.
    El estado se elige al azar.
    de la lista dice ["excelente", "bueno", "advertencia", "defectuoso", "muerto", "desconocido"]
    el codigo hash es de tipo md5 se genero a partir de la fecha actual, el idd, el tipo de componente
    y el estado del componente
    validacion para el estado y el idd unknown para que cuando se detecte sea marcado como desconocido
    en las areas del tipo, el estado y el hash
    """
    states = ["excellent", "good", "warning", "faulty", "killed", "unknown"]
    components = ["satellites", "spacesships", "space suits", "space vehicles"]
    current_date = datetime.now().strftime("%d%m%y%H%M%S")
    device_status = random.choice(states)
    type_components = random.choice(components)
    h = hashlib.md5()
    h.update(current_date.encode('utf-8'))
    h.update(idd.encode('utf-8'))
    h.update(type_components.encode('utf-8'))
    h.update(device_status.encode('utf-8'))
    hash = h.hexdigest()
    if idd == "APLUnknown" or device_status == "unknown":
        content = f"""
                Fecha: {current_date} 
                IDD: {idd}
                Tipo de dispositivo: "unknown"
                Estado del dispositivo: "unknown"
                Hash: "unknown"
                """
    else:
        content = f"""
                Fecha: {current_date} 
                IDD: {idd}
                Tipo de dispositivo: {type_components}
                Estado del dispositivo: {device_status}
                Hash: {hash}
                """
    return content


def synchronization():
    """
        Esta función crea una carpeta llamada 'dispositivos' en el director actual
        Si la carpeta se crea correctamente, registra un mensaje de información.
        Si la carpeta ya existe, registra un mensaje de advertencia.
        Si ocurre alguna otra excepción durante la creación de la carpeta
        registra un mensaje de advertencia con los detalles del error.
    """
    folder_name = "devices"
    try:
        os.mkdir(folder_name)
        logging.info("Carpeta {} creada con éxito".format(folder_name))
    except FileExistsError:
        logging.warning("La carpeta {} ya existe".format(folder_name))
    except Exception as e:
        logging.warning("Error al crear la carpeta: {}".format(e))

        
def generate():
    """
    Genera archivos y carpetas en el directorio 'dispositivos'.
    Esta función crea una subcarpeta con un nombre basado en la fecha y hora actuales.
    dentro del directorio 'dispositivos'. Luego genera entre 1 y 10 archivos cada 2 minutos,
    cada uno contiene información sobre el estado del dispositivo.
    cada lote de archivos esta marcado de 1 al numero maximo de archivos escogidos aleatoriamente
    en cada lote el contador se reinicia para realizar la misma operacion
    """
    folder_name = "devices"
    current_date = datetime.now().strftime("%d%m%y%H%M%S")
    subfolder_name = os.path.join(folder_name, current_date)
    os.mkdir(subfolder_name)

    file_to_generate = random.randint(1, 10)
    for _ in range(file_to_generate):
        number_files = _ + 1
        missions = ["OrbitOne", "ColonyMoon", "VacMars", "GalaxyTwo" , "Unknown"]
        idd = random.choice(missions)
        file_name = f"APL{idd}-0000{number_files}.log"
        path_file = os.path.join(subfolder_name, file_name)

        try:
            with open(path_file, 'w') as archive:
                content = generate_content_files(file_name.split('-')[0])
                archive.write(content)
            logging.info("Archivo {} creado con éxito".format(file_name))
        except Exception as e:
            logging.warning("Error al crear el archivo {}: {}".format(file_name, e))


class apl_main():
    """
    Se define una clase llamada apl_main, que encapsula el método principal del programa.
    El decorador @staticmethod indica que este método se puede llamar en la clase sin
    creando una instancia del mismo.
    """

    @staticmethod
    def main():
        """
        Inicia el ciclo principal del programa.
        El bucle principal llama continuamente a la función 'Sincronización' para crear la carpeta 'dispositivos'
        y generar archivos de acuerdo con los requisitos especificados. Luego llama a la función 'generar'.
        para crear archivos dentro de la carpeta 'dispositivos'. Después de cada iteración, el bucle espera 20 segundos.
        """
        synchronization()
        
        while True:
            
            generate()

            time.sleep(20)

if __name__ == "__main__":
    """
    configura el sistema de registro para mostrar mensajes de nivel INFO o superior.
    Esto proporciona información sobre la ejecución del script, como mensajes de éxito o advertencias.
    Se llama al método estático main() de la clase apl_main para iniciar la ejecución del programa.
    """
    logging.basicConfig(level=logging.INFO)

    apl_main.main()
