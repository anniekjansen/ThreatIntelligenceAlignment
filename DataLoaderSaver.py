import pandas as pd
from pathlib import Path

class DataLoaderSaver:

    def load_dataset(self, dataset_prefix, dataset_suffix, seperator=","):
        data_path = Path("./intermediate_datafiles/")
        dataset = f"{dataset_prefix}_advisories_{dataset_suffix}.csv"

        try:
            data = pd.read_csv(data_path / dataset, index_col=0, sep=seperator)
        except IOError as e:
            print("File not found!")
            raise e

        return data
    
    def save_dataset(self, data, dataset_prefix, dataset_suffix, seperator=","):
        data_path = Path("./intermediate_datafiles/")
        dataset = f"{dataset_prefix}_advisories_{dataset_suffix}.csv"

        data.to_csv(data_path / dataset, sep=seperator)

