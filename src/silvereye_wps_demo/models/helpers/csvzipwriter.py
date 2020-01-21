import csv
from typing import List, Tuple
import numpy as np

ZippedList = List[Tuple]


class CSVZipWriter:
    """Serializes a list of tuples into a csv file."""

    def __init__(self, fname: str, fieldnames: List[str], data: ZippedList) -> None:
        """
        :para fname: str, filename to write to
        :param fieldnames: list of names for the column headers
        :param data: List with zipped data
        """
        self.fname = fname
        self.fieldnames = fieldnames
        self.data = data

    def write(self):
        with open(self.fname, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.fieldnames)
            for row in self.data:
                writer.writerow(row)


if __name__ == '__main__':

    file_name = '../data/outfilezzz.csv'
    field_names = ["col 1", "col 2", "col 3"]
    data = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    app = CSVZipWriter(file_name, field_names, data)
    app.write()
