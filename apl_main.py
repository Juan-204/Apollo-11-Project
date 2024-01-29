import hashlib

import logging

import os

import random

from datetime import datetime

from typing import List, Tuple, Dict, Any, Union

import glob

import re
import shutil

import time


folder_name: str = "devices"
folder_backup: str = "backup"
current_date: str = datetime.now().strftime("%d%m%y%H%M%S")
current_route: str = os.getcwd()
subfolder_name: str = os.path.join(folder_name, current_date)


def generate_content_files(idd: str) ->str:
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
    validacion para el idd unknown para que cuando se detecte sea marcado como desconocido
    en las areas del tipo, el estado y el hash
    """
    states: List[str] = ["excellent", "good", "warning", "faulty", "killed", "unknown"]
    components: List[str] = ["satellites", "spacesships", "space suits", "space vehicles"]
    current_date: str = datetime.now().strftime("%d%m%y%H%M%S")
    if idd.lower() == "aplunknown":
        type_components: str = "unknown"
        device_status: str = "unknown"
        hash_value: str = "unknown"
    else:
        device_status = random.choice(states)
        type_components = random.choice(components)
        h = hashlib.md5()
        h.update(current_date.encode('utf-8'))
        h.update(idd.encode('utf-8'))
        h.update(type_components.encode('utf-8'))
        h.update(device_status.encode('utf-8'))
        hash_value = h.hexdigest()

    content = f"""
            Fecha: {current_date}
            IDD: {idd}
            Tipo de dispositivo: {type_components}
            Estado del dispositivo: {device_status}
            Hash: {hash_value}
            """
    return content


def synchronization(folder_name: str, folder_backup: str) -> None:
    """
    Esta función crea una carpeta llamada 'dispositivos' en el director actual
    Si la carpeta se crea correctamente, registra un mensaje de información.
    Si la carpeta ya existe, registra un mensaje de advertencia.
    Si ocurre alguna otra excepción durante la creación de la carpeta
    registra un mensaje de advertencia con los detalles del error.
    """
    try:
        os.mkdir(folder_name)
        os.mkdir(folder_backup)
        logging.info("Carpeta {} creada con éxito".format(folder_name))
        logging.info("Carpeta {} creada con éxito".format(folder_backup))
    except FileExistsError:
        logging.warning("La carpeta {} ya existe".format(folder_name))
        logging.warning("La carpeta {} ya existe".format(folder_backup))
    except Exception as e:
        logging.warning("Error al crear la carpeta: {}".format(e))


def file_analysis(folder_name: str, current_date: str) -> str:
    """
    analizis de los archivos .log que contiene la informacion de las misiones
    para generar un archivo con la informacion condensada, primero se itera
    sobre las subcarpetas en la carpeta devices para
    poder encontrar los archivos con la extension, luego por medio de expresiones
    regulares extraemos la informacion y todo lo condensamos en un diccionario de
    diccionarios para posteriormente establecer contadores para que agregen las ocurrencias
    encontradas, todo esto se escribe en
    un archivo APLSTATS-REPORT con la fecha actual para que la
    informacion de cada lote de archivos sea mas legible y global
    Args:
        subfolder_name (_str_): contiene la ruta de las subcarpetas dentro de la carpeta raiz
        current_date (_str_): contiene la fecha actual del sistema
    """

    extension: str = os.path.join(folder_name, '**', '*.log')
    archive_log: List[str] = glob.glob(extension, recursive=True)
    report = {}
    count_unk: int = 0

    for archive_path in archive_log:
        try:
            with open(archive_path, 'r') as archive_file:
                content: str = archive_file.read()
                match_idd = re.search(r'IDD: (\w+)', content)
                match_tipe_components = re.search(r'Tipo de dispositivo: (\w+)', content)
                match_state_component = re.search(r'Estado del dispositivo: (\w+)', content)
                match_unknown = re.search(r'IDD: (APLUnknown)', content)

                if match_unknown:
                    idd: str = match_unknown.group(1)
                    if idd == "APLUnknown":
                        count_unk += 1

                if match_idd and match_tipe_components and match_state_component:
                    idd = match_idd.group(1)
                    tipe_components: str = match_tipe_components.group(1)
                    state_components: str = match_state_component.group(1)
                    if idd not in report:
                        report[idd] = {tipe_components: {states: 0 for states in [
                            "excellent", "good", "warning", "faulty", "killed", "unknown"]}}
                    elif tipe_components not in report[idd]:
                        report[idd][tipe_components] = {states: 0 for states in [
                            "excellent", "good", "warning", "faulty", "killed", "unknown"]}
                    report[idd][tipe_components][state_components] += 1
        except Exception as e:
            print(f"Error al leer el archivo {archive_path}: {e}")

    total_unknown_counts: Dict[str, int] = {}
    for idd, components in report.items():
        total_unknown_count: int = 0
        for component_states in components.values():
            total_unknown_count += component_states.get("unknown", 0)
        total_unknown_counts[idd] = total_unknown_count

    report_name: str = f"APLSTATS-REPORT-{current_date}.log"
    path_file: str = os.path.join(folder_name, report_name)
    with open(path_file, 'w') as report_file:
        report_file.write("La cantidad de misiones que no se encuentran en el registro son: {}\n".format(count_unk))
        report_file.write("\nMisiones con Mayor Cantidad de Estados Desconocidos:\n")
        if total_unknown_counts:
            ranking_unknown: List[Tuple[str, int]] = sorted(total_unknown_counts.items(), key=lambda x: x[1], reverse=True)
            for mission, unknown_count in ranking_unknown:
                report_file.write(f"\tMisión: {mission}, Cantidad de 'unknown': {unknown_count}\n")
        else:
            report_file.write("\tNo hay misiones con estados 'unknown'.\n")

        for idd, components in report.items():
            report_file.write(f"\nMisión: {idd}\n")
            for tipe, state in components.items():
                report_file.write(f"\tTipo de dispositivo: {tipe}\n")
                for states_2, count in state.items():
                    report_file.write(f"\t\tEstado '{states_2}': {count}\n")

    return report_name


def move_backup(report: str, current: str, folder_name: str, backup: str) -> None:

    extension: str = os.path.join(current, folder_name)
    extension: str = os.path.abspath(extension)

    now_route: str = os.path.join(current, folder_name)
    move_route: str = os.path.join(current, backup)

    get_files: List[str] = os.listdir(extension)

    print(get_files)

    for archive in get_files:

        if re.match(r"APLSTATS", archive):
            logging.info(f"archivo ignorado con exito {report}")
            continue
        shutil.move(now_route + "\\" + archive, move_route)
        logging.info("los archivos fueron analizados y movidos con exito")


def generate(folder_name: str) -> None:
    """
    Genera archivos y carpetas en el directorio 'dispositivos'.
    Esta función crea una subcarpeta con un nombre basado en la fecha y hora actuales.
    dentro del directorio 'dispositivos'. Luego genera entre 1 y 10 archivos cada 2 minutos,
    cada uno contiene información sobre el estado del dispositivo.
    cada lote de archivos esta marcado de 1 al numero maximo de archivos escogidos aleatoriamente
    en cada lote el contador se reinicia para realizar la misma operacion
    """
    current_date: str = datetime.now().strftime("%d%m%y%H%M%S")
    subfolder_name: str = os.path.join(folder_name, current_date)
    os.mkdir(subfolder_name)

    file_to_generate: int = random.randint(1, 10)
    for _ in range(file_to_generate):
        number_files: int = _ + 1
        missions: List[str] = ["OrbitOne", "ColonyMoon", "VacMars", "GalaxyTwo", "Unknown"]
        idd: str = random.choice(missions)
        file_name: str = f"APL{idd}-0000{number_files}.log"
        path_file: str = os.path.join(subfolder_name, file_name)

        try:
            with open(path_file, 'w') as archive:
                content: str = generate_content_files(file_name.split('-')[0])
                archive.write(content)
            logging.info("Archivo {} creado con éxito".format(file_name))
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
        try:
            synchronization(folder_name, folder_backup)

            while True:

                generate(folder_name)
                report = file_analysis(folder_name, current_date)

                time.sleep(10)
        except KeyboardInterrupt:
            move_backup(report, current_route, folder_name, folder_backup)


if __name__ == "__main__":
    """
    configura el sistema de registro para mostrar mensajes de nivel INFO o superior.
    Esto proporciona información sobre la ejecución del script, como mensajes de éxito o advertencias.
    Se llama al método estático main() de la clase apl_main para iniciar la ejecución del programa.
    """
    logging.basicConfig(level=logging.INFO)

    AplMain.main()
