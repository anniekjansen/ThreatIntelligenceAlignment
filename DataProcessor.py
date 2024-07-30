import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import ast
import string

class DataProcessor:

    def drop_columns(self, data, columns_to_drop):
        data = data.drop(columns=columns_to_drop)
        return data
    
    def drop_duplicates(self, data):
        data = data.drop_duplicates(ignore_index=True)
        return data
    
    def drop_missing_values(self, data):
        data = data.dropna()
        return data

    def object_to_datetime(self, data, column):
        for row in range(len(data)):
            date_string = data.loc[row, column]
            if column == 'Uitgiftedatum':
                datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
            else:
                datetime_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        data.loc[row, column] = datetime_obj
        data[column] = pd.to_datetime(data[column], utc=True)
        return data
    
    def string_to_list(self, data, columns):
        for col in columns:
            data[col] = data[col].apply(ast.literal_eval)
        return data

    def values_to_None(self, data, columns):
        for col in columns:
            data[col] = data[col].apply(lambda x: None if x in ([], ['niet beschikbaar'], ["-"], ['-'], "*", "-") else x)
        return data
        
    def fix_cve_id(self, cve_id):
        cve_id_fixed = cve_id.translate(str.maketrans("", "", string.punctuation.replace("-", "")))
        return cve_id_fixed
     
    def valid_cve_id(self, cve_id):
        if (len(cve_id) in [13, 14] and cve_id[:3].isalpha() and cve_id[3] == "-" and all(c.isdigit() or c == "-" for c in cve_id[4:])):
            valid_cve_id = cve_id
            return valid_cve_id
        else:
            return None
