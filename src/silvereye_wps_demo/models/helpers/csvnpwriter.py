import csv
from typing import List
import numpy as np

Matrix2D = List[List[float]]

class CSVNpWriter:
    """Serializes a NumPy array into a csv file."""

    def __init__(self, fname: str, fieldnames: List, data: Matrix2D) -> None:
        """
        :para fname: str, filename to write to
        :param fieldnames: list of names for the column headers
        :param data: Matrix2D, NumPy Array with the data (must be 2d)
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

    file_name = '../data/outfile.csv'
    field_names = ["col 1", "col 2", "col 3"]
    data = np.array([
                [1, 2, 3.0],   # coerces data to float
                [4, 5, 6.0],
                [7, 8, 9.0]])
    app = CSVNpWriter(file_name, field_names, data)
    app.write()
