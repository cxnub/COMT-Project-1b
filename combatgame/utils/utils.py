"""Utility functions for project."""
import csv

def csv_to_dict(file_path: str, key_column: str) -> dict:
    """Reads csv config file and store it in a dictionary.
    
    Parameters
    ----------
    file_path : str
        The file path of the csv file.
    key : str
        The column for keys.
    """
    result_dict = {}

    # open the CSV file
    with open(file_path, "r", encoding="utf-8") as file:
        # converts csv file to python dictionary
        csv_to_dict_reader = csv.DictReader(file)

        # iterate over each row and convert it to a dictionary
        for row in csv_to_dict_reader:

            # assign the key name to its dict of attributes
            key = str(row.pop(key_column))
            result_dict[key] = row

    return result_dict
