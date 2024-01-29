import unittest
from unittest.mock import patch
from datetime import datetime
from io import StringIO
import os
import shutil

from apl_main import (
    generate_content_files,
    synchronization,
    file_analysis,
    move_backup,
    generate,
    AplMain,
)


class TestAplFunctions(unittest.TestCase):

    def setUp(self):
        self.folder_name = "devices"
        self.folder_backup = "backup"
        self.current_date = datetime.now().strftime("%d%m%y%H%M%S")
        self.subfolder_name = os.path.join(self.folder_name, self.current_date)
        os.makedirs(self.folder_name, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.folder_name, ignore_errors=True)

    def test_generate_content_files(self):
        content = generate_content_files("OrbitOne")
        self.assertIn("Fecha:", content)
        self.assertIn("IDD: OrbitOne", content)
        self.assertIn("Tipo de dispositivo:", content)
        self.assertIn("Estado del dispositivo:", content)
        self.assertIn("Hash:", content)

    def test_synchronization(self):
        with patch("builtins.print") as mock_print:
            synchronization(self.folder_name, self.folder_backup)
            mock_print.assert_called_with("Carpeta {} creada con éxito".format(self.folder_name))

    def test_file_analysis(self):
        # TODO: Implement test for file_analysis function
        pass

    def test_move_backup(self):
        report_name = "APLSTATS-REPORT-{}.log".format(self.current_date)
        report_path = os.path.join(self.folder_name, report_name)
        open(report_path, 'w').close()  # Create an empty report file

        with patch("builtins.print") as mock_print:
            move_backup(report_name, self.current_date, self.folder_name, self.folder_backup)
            mock_print.assert_called_with("archivo ignorado con exito {}".format(report_name))

    def test_generate(self):
        generate(self.folder_name)
        generated_files = os.listdir(self.subfolder_name)
        self.assertTrue(generated_files)

    def test_AplMain_main(self):
        # Mock the keyboard interrupt to test graceful termination
        with patch("apl_main.move_backup") as mock_move_backup:
            with patch("apl_main.generate") as mock_generate:
                with patch("time.sleep"):
                    AplMain.main()
                    mock_move_backup.assert_called_once()


if __name__ == "__main__":
    unittest.main()
