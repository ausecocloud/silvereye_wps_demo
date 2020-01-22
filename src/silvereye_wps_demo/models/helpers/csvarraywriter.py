import csv
from typing import List


class CSVArrayWriter:
    """Serializes a Python array into a csv file."""

    def __init__(self, file_name: str, field_names: List, data: List) -> None:
        """
        :para file_name: str, filename to write to
        :param field_names: list of names for the column headers
        :param data: List, Python Array with the data by columns
        """
        self.file_name = file_name
        self.field_names = field_names
        self.data = data

    def write(self):
        with open(self.file_name, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.field_names)
            row_count = len(self.data[-1])
            col_count = len(self.data)
            for i in range(row_count):
                # make a row with data from columns
                row = []
                for j in range(col_count):
                    # print(j)
                    row.append(self.data[j][i])  # data is by cols
                writer.writerow(tuple(row))


if __name__ == '__main__':

    file_name = '../data/outfile_cols.csv'
    field_names = ["col 1", "col 2", "col 3"]
    data = [[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12]]
    app = CSVArrayWriter(file_name, field_names, data)
    app.write()
