import hashlib
import logging
from msilib.schema import Component

import os

import random

from datetime import datetime, timedelta

import time

# def generate_file_names():
#     """ 
#     Generates file names for space missions.
#     Returns a string with the file name APL{idd}-0000{number_files}.log
#     The mission is selected randomly
#     """
#     missions = ["OrbitOne", "ColonyMoon", "VacMars", "GalaxyTwo"]
#     idd = random.choice(missions)
#     number_files = random.randint(1, 1000)
#     return f"APL{idd}-0000{number_files}.log"


def generate_content_files(idd):
    """
    Generates content for device state files.
    Args idd: string as device identifier
    Returns str: a string containing information about the state of the device,
    including the current date,device identifier (IDD) and device status.
    The status is randomly chosen 
    from the list states["excellent", "good", "warning", "faulty", "killed", "unknown"]
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


def Synchronization():
    """
    This function create a folder named 'devices' in the current director
    If the folder is created successfully, it logs an information message.
    If the folder already exists, it logs a warning message.
    If any other exception occurs during the folder creation
    it logs a warning message with the error details.
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
    Generates files and folders in the 'devices' directory.
    This function creates a subfolder with a name based on the current date and time
    inside the 'devices' directory. It then generates between 1 and 10 files every 2 minutes,
    each containing information about the device status.
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
    """A class called apl_main is defined, which encapsulates the main method of the program.
    The @staticmethod decorator indicates that this method can be called on the class without
    creating an instance of it.
    """

    @staticmethod
    def main():
        """
        Initiates the main program loop.
        The main loop continuously calls the 'Synchronization' function to create the 'devices' folder
        and generate files according to specified requirements. It then calls the 'generate' function
        to create files within the 'devices' folder. After each iteration, the loop waits for 20 seconds
        """
        Synchronization()
        
        while True:
            
            generate()

            time.sleep(20)

if __name__ == "__main__":
    """
    configures the logging system to display messages of INFO level or higher.
    This provides information about the execution of the script, such as success messages or warnings.
    The static main() method of the apl_main class is called to start the program execution.
    """
    logging.basicConfig(level=logging.INFO)

    apl_main.main()
