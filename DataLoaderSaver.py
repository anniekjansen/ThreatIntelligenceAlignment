import pandas as pd
from pathlib import Path

class DataLoaderSaver:

    def load_dataset(self, dataset_prefix, dataset_suffix, seperator=","):
        data_path = Path("./intermediate_datafiles/")
        dataset = f"{dataset_prefix}_advisories_{dataset_suffix}"

        try:
            if dataset_suffix == 'initial':
                data = pd.read_csv((data_path / dataset).with_suffix('.csv'), index_col=0, sep=seperator)
            else:
                data = pd.read_json((data_path / dataset).with_suffix('.json'))
        except IOError as e:
            print("File not found!")
            raise e

        return data
    
    def save_dataset(self, data, dataset_prefix, dataset_suffix, seperator=","):
        data_path = Path("./intermediate_datafiles/")
        dataset = f"{dataset_prefix}_advisories_{dataset_suffix}.json"

        # data.to_csv(data_path / dataset, sep=seperator)
        data.to_json(data_path / dataset, orient='records', date_format='iso')
        print("Dataset saved succesfully!")
