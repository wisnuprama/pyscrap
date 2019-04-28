import csv
import os


def serialize_to_csv(filename: str, data: dict):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as csv_file:
        fieldnames = data.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
