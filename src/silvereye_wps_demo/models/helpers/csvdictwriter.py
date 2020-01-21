import csv
from typing import List, Dict
ListDict = List[Dict]


class CSVDictWriter:
    """Serializes a NumPy array into a csv file."""

    def __init__(self, fname: str, fieldnames: List, data: ListDict) -> None:
        """
        :param fname: str, filename to write to
        :param fieldnames: list of names for the column headers
        :param data: ListDict, list of dictionary data structure with the data
        """
        self.fname = fname
        self.fieldnames = fieldnames
        self.data = data

    def write(self) -> None:
        """writes data to the file"""
        with open(self.fname, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)


if __name__ == '__main__':

    file_name = '../data/outfile2.csv'
    field_names = ["col 1", "col 2", "col 3"]
    data = [
        {"col 1": 1.0, "col 2": 2.0, "col 3": 3.0},
        {"col 1": 4.0, "col 2": 5.0, "col 3": 6.0},
        {"col 1": 7.0, "col 2": 8.0, "col 3": 9.0}
    ]

    app = CSVDictWriter(file_name, field_names, data)
    app.write()
