""" This module reads *.csv files from zip file and creates combined csv file"""
import csv
import os
import shutil
from pathlib import Path
from zipfile import ZipFile
import configparser
import pdb
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


class Smartcsv:

    def process_csv_files(self):
        """ process csv files to create single combined file"""
        logging.info("Statrted reading csv files")

        data_file_path_obj = self.get_data_file_path()

        if(not data_file_path_obj.exists()):
            logging.info(
                "Data file is missing to process please place .zip file under data folder")
        else:
            logging.info(f"Started processing the {data_file_path_obj}  file")
            logging.info(
                f" extracted data under below folder:  {data_file_path_obj.stem}")
            old_dir_path = Path()/data_file_path_obj.stem
            if old_dir_path.exists() and old_dir_path.is_dir():
                shutil.rmtree(old_dir_path)
            path_extracted_data, csv_files = self.get_csv_files(
                data_file_path_obj)
            self.write_csv_files_to_single_file(path_extracted_data, csv_files)

    def get_data_file_path(self):
        """ Get test data file path"""
        # pdb.set_trace()

        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, r'configuration.txt')
        # logging.info(f"Current folder : {thisfolder}")
        # logging.info(initfile)
        config = configparser.ConfigParser()
        config.read(initfile)
        test_file_data_path = config.get(
            'FilePath-info', 'test_file_data_path')
        logging.info(
            f" Reading test data from this location : {test_file_data_path}")

        data_file_path_obj = Path(os.path.join(
            thisfolder, "..", test_file_data_path))
        # /Users/pruthviraj/Python/Pruthvi_Py_CSV/pruthvipycsv
        # /Users/pruthviraj/Python/Pruthvi_Py_CSV/data/Engineering Test Files.zip
        logging.info(data_file_path_obj)
        return data_file_path_obj

    def write_csv_files_to_single_file(self, path_extracted_data, csv_files):
        """ Reading each CSV at a time from extracted folder and writing into single combined file"""
        try:
            with open(os.path.join(path_extracted_data/"Combined.csv"), "w") as csvwriterfile:
                csvwriter = csv.writer(csvwriterfile)
                fields = ["Source IP", "Environment"]
                csvwriter.writerow(fields)
                for eachcsvfile in csv_files:
                    if not eachcsvfile.name == "Combined.csv":
                        logging.info(
                            f" current file processing is .... {path_extracted_data/eachcsvfile.name}")
                        with open(os.path.join(path_extracted_data/eachcsvfile.name), "r", encoding="utf-8-sig") as csvfile:
                            reader = csv.DictReader(csvfile)
                            for row in reader:
                                data_to_write = [
                                    row["Source IP"], eachcsvfile.name]
                                csvwriter.writerow(
                                    data_to_write)
                        logging.info(
                            f"*** Processing completed for file: {path_extracted_data/eachcsvfile.name} ***")
            return True
        except Exception as ex:
            logging.error("Something went wrong when writing to the file")
            return False

    def get_csv_files(self, path_obj):
        """ Extract only .csv files from the zip folder"""
        with ZipFile(path_obj) as zip_obj:
            zip_obj.extractall(path_obj.stem)
            path_of_extracted_data = Path()/path_obj.stem/path_obj.stem
            logging.info(path_of_extracted_data.is_dir())
            csv_files = [
                each_item for each_item in path_of_extracted_data.rglob("*.csv")]
        return path_of_extracted_data, csv_files


smartcsv_obj = Smartcsv()
smartcsv_obj.process_csv_files()
