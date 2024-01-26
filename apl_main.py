import hashlib

import logging

import os

import random

from datetime import datetime

import glob

import re

import time

folder_name = "devices"
current_date = datetime.now().strftime("%d%m%y%H%M%S")
subfolder_name = os.path.join(folder_name, current_date)

def generate_content_files(idd):
    """
    Genera contenido para archivos de estado del dispositivo.
    Args idd: cadena como identificador de dispositivo
    Devuelve str: una cadena que contiene información sobre el estado del dispositivo,
    incluyendo la fecha actual, el identificador del dispositivo (IDD)
    y el estado del dispositivo.
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


def synchronization(folder_name):
    """
    Esta función crea una carpeta llamada 'dispositivos' en el director actual
    Si la carpeta se crea correctamente, registra un mensaje de información.
    Si la carpeta ya existe, registra un mensaje de advertencia.
    Si ocurre alguna otra excepción durante la creación de la carpeta
    registra un mensaje de advertencia con los detalles del error.
    """
    try:
        os.mkdir(folder_name)
        logging.info("Carpeta {} creada con éxito".format(folder_name))
    except FileExistsError:
        logging.warning("La carpeta {} ya existe".format(folder_name))
    except Exception as e:
        logging.warning("Error al crear la carpeta: {}".format(e))

def file_analysis(subfolder_name,current_date):
    """
    analizis de los archivos .log que contiene la informacion de las misiones para generar un archivo con la informacion
    condensada
    Args:
        subfolder_name (_str_): contiene la ruta de las subcarpetas dentro de la carpeta raiz
        current_date (_str_): contiene la fecha actual del sistema
    """
    
    extension = os.path.join(subfolder_name, '*.log')
    archive_log = glob.glob(extension, recursive=True)
    report = {}
    
    for archive_path in archive_log:
        try:
            with open(archive_path, 'r') as archive_file:
                content = archive_file.read()
                match_idd = re.search(r'IDD: (\w+)', content)
                match_tipe_components = re.search(r'Tipo de dispositivo: (\w+)', content)
                match_state_component = re.search(r'Estado del dispositivo: (\w+)', content)
                if match_idd and match_tipe_components and match_state_component:
                    idd = match_idd.group(1)
                    tipe_components = match_tipe_components.group(1)
                    state_components = match_state_component.group(1)
                    if idd not in report:
                        report[idd] = {tipe_components: {states: 0 for states in ["excellent", "good", "warning", "faulty", "killed", "unknown"]}}
                    elif tipe_components not in report[idd]:
                        report[idd][tipe_components] = {states: 0 for states in ["excellent", "good", "warning", "faulty", "killed", "unknown"]}
                    report[idd][tipe_components][state_components] += 1
        except Exception as e:
            print(f"Error al leer el archivo {archive_path}: {e}")
    report_name = f"APLSTATS-REPORT-{current_date}.log"
    path_file = os.path.join(subfolder_name, report_name)
    
    with open(path_file, 'w') as report_file:
        for idd, components in report.items():
            report_file.write(f"Misión: {idd}\n")
            for tipe, state in components.items():
                report_file.write(f"\tTipo de dispositivo: {tipe}\n")
                for states_2, count in state.items():
                    report_file.write(f"\t\tEstado '{states_2}': {count}\n")
        
def generate(folder_name):
    """
    Genera archivos y carpetas en el directorio 'dispositivos'.
    Esta función crea una subcarpeta con un nombre basado en la fecha y hora actuales.
    dentro del directorio 'dispositivos'. Luego genera entre 1 y 10 archivos cada 2 minutos,
    cada uno contiene información sobre el estado del dispositivo.
    cada lote de archivos esta marcado de 1 al numero maximo de archivos escogidos aleatoriamente
    en cada lote el contador se reinicia para realizar la misma operacion
    """
    current_date = datetime.now().strftime("%d%m%y%H%M%S")
    subfolder_name = os.path.join(folder_name, current_date)
    os.mkdir(subfolder_name)

    file_to_generate = random.randint(1, 10)
    for _ in range(file_to_generate):
        number_files = _ + 1
        missions = ["OrbitOne", "ColonyMoon", "VacMars",
                    "GalaxyTwo", "Unknown"]
        idd = random.choice(missions)
        file_name = f"APL{idd}-0000{number_files}.log"
        path_file = os.path.join(subfolder_name, file_name)

        try:
            with open(path_file, 'w') as archive:
                content = generate_content_files(file_name.split('-')[0])
                archive.write(content)
            logging.info("Archivo {} creado con éxito".format(file_name))
            file_analysis(subfolder_name, current_date)
        except Exception as e:
            logging.warning("Error al crear el archivo {}: {}".format(file_name, e))
            


class AplMain():
    """
    Se define una clase llamada apl_main, que encapsula el método principal del programa.
    El decorador @staticmethod indica que este método se puede llamar en la clase sin
    creando una instancia del mismo.
    """

    @staticmethod
    def main():
        """
        antes de iniciar el ciclo principal se llama a la funcion "synchronization" para crear la carpeta dispositivos
        si ya no esta creada previamente
        Inicia el ciclo principal del programa.
        se llama a la funcion "generar" en el ciclo infinito
        para crear archivos dentro de la carpeta 'dispositivos'. Después de cada iteración, el bucle espera 20 segundos.
        """
        synchronization(folder_name)
        
        while True:
            
            generate(folder_name)
            time.sleep(20)


if __name__ == "__main__":
    """
    configura el sistema de registro para mostrar mensajes de nivel INFO o superior.
    Esto proporciona información sobre la ejecución del script, como mensajes de éxito o advertencias.
    Se llama al método estático main() de la clase apl_main para iniciar la ejecución del programa.
    """
    logging.basicConfig(level=logging.INFO)

    AplMain.main()
