import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:

    def print_column_names(self, data):
        print("Columns:")
        for column in data.columns:
            print(column)

    def print_info(self, data):
        print(data.shape) # rows and columns
        print(data.head())
        print(data.tail())
        print(data.iloc[0])
        print(data.iloc[35683])
        print(data.dtypes)
        print(data.nunique())
        print(data.isnull().sum())
        print("Total # of missing values:", data.isnull().sum().sum())

    def print_histogram(self, data, column_title):
        data[column_title].value_counts().plot(kind='bar')
        plt.xticks(rotation=15)
        plt.show()

    def print_barchart_kans_schade(self, data, columns):
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df1['Kans'] = data["Kans"]
        df2['Schade'] = data["Schade"]

        name_sort = {'Low':0,'Medium':1,'High':2}
        df1['name_sort'] = df1['Kans'].map(name_sort)
        df2['name_sort'] = df2['Schade'].map(name_sort)
     
        df1 = df1.sort_values(by=['name_sort'])
        df2 = df2.sort_values(by=['name_sort'])

        width = 0.25
        df1['Kans'].value_counts(sort=False).plot(kind='bar', width = width, position=1, title="Bar Chart Kans & Schade")
        df2['Schade'].value_counts(sort=False).plot(kind='bar', color='skyblue', position=0, width = width) 
        plt.legend(["Kans", "Schade"])
        plt.ylabel("Counts")
        plt.xlabel("")
        plt.xticks(rotation ='horizontal')
        plt.savefig("./figures/BarChartKansSchade")
        plt.show()

    def print_selected_columns(self, data, columns): 
        print(data[columns])
    
    def print_selected_cell(self, data, rownumber, column_title):
        print(data.loc[rownumber, column_title])
        print(data.iloc[rownumber])

    def print_selected_value(self, data, column_title, value):
        print(data.loc[data[column_title] == value])

    def check_duplicates(self, data):
        print('Total # of duplicates:', data.duplicated().sum())

    def check_duplicates_columns(self, data, columns):
        print(data.duplicates())
        for col in columns:
            print(col, ':', data.duplicated(subset=[col]).sum(), 'duplicates')

    def check_uniques(self, data):
        print(data.nunique())

    def check_uniques_columns(self, data, columns):
        for col in columns:
            data_col = data[col]
            print(col, ':', data_col.nunique(), 'unique values')
