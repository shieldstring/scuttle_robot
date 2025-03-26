import csv
from datetime import datetime
import logging
class Logger:
    def __init__(self, filename="log.csv"):
        self.filename = filename

    def log_data(self, data):
        with open(self.filename, "a") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now()] + data)


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )