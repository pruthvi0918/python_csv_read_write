import pdb
from pruthvipycsv.smart_csv import Smartcsv


smart_csv_obj = Smartcsv()

# if pytest not able locate module then execute below commands to set root directory for pythonpath.
# export PYTHONPATH=. pytest


def test_get_csv_files():
    pdb.set_trace()
    assert smart_csv_obj.get_data_file_path().exists()


def test_get_csv_files():
    path_extracted_data, csv_files = smart_csv_obj.get_csv_files(
        smart_csv_obj.get_data_file_path())
    assert not len(csv_files) == 0, "the list is non empty"


def test_write_csv_files_to_single_file():
    path_extracted_data, csv_files = smart_csv_obj.get_csv_files(
        smart_csv_obj.get_data_file_path())
    assert smart_csv_obj.write_csv_files_to_single_file(
        path_extracted_data, csv_files) is True
