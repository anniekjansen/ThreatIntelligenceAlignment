import pandas as pd
from pathlib import Path

class DataLoaderSaver:

    def load_dataset(self, dataset_name, seperator=","):
        data_path = Path("./intermediate_datafiles/")
        dataset = f"NCSC_advisories_{dataset_name}.csv"

        try:
            data = pd.read_csv(data_path / dataset, index_col=0, sep=seperator)
        except IOError as e:
            print("File not found!")
            raise e

        return data
    
    def save_dataset(self, data, dataset_name, seperator=","):
        data_path = Path("./intermediate_datafiles/")
        dataset = f"NCSC_advisories_{dataset_name}.csv"

        data.to_csv(data_path / dataset, sep=seperator)

