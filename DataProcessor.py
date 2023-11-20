import pandas as pd
import datetime

class DataProcessor:

    def drop_columns(self, data, columns_to_drop):
        data = data.drop(columns=columns_to_drop)
        return data
    
    def drop_duplicates(self, data):
        data = data.drop_duplicates(ignore_index=True)
        return data

    def object_to_datetime(self, data):
        for row in range(len(data)):
            date_string = data.loc[row,'Uitgiftedatum']
            datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
            data.loc[row,'Uitgiftedatum'] = datetime_obj
        data['Uitgiftedatum']= pd.to_datetime(data['Uitgiftedatum'],utc=True)
        return data
    
    
    