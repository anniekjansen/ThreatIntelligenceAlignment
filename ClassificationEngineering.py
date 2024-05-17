import pandas as pd

class ClassificationEngineering:

    def create_change_columns(self, df, kans_schade):
        df[kans_schade + ' no change'] = 0
        df[kans_schade + ' unjustified change'] = 0
        df[kans_schade + ' unimportant change'] = 0
        df[kans_schade + ' justified+important change'] = 0

        for row in range(len(df)):
            if df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new'] and df.loc[row, kans_schade + ' old'] == df.loc[row, kans_schade + ' new']:
                df.loc[row, kans_schade + ' no change'] = 1
            elif (df.loc[row,'Beschrijving old'] == df.loc[row, 'Beschrijving new']) and (df.loc[row, kans_schade + ' old'] != df.loc[row, kans_schade + ' new']):
                df.loc[row, kans_schade + ' unjustified change'] = 1
            elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row, kans_schade + ' old'] == df.loc[row, kans_schade + ' new']):
                df.loc[row, kans_schade + ' unimportant change'] = 1
            elif (df.loc[row,'Beschrijving old'] != df.loc[row, 'Beschrijving new']) and (df.loc[row, kans_schade + ' old'] != df.loc[row, kans_schade + ' new']):
                df.loc[row, kans_schade + ' justified+important change'] = 1

    def print_overview(self, df, kans_schade):
        print(kans_schade)
        print("No change:", df[kans_schade + ' no change'].sum())
        print("Unjustified change:", df[kans_schade + ' unjustified change'].sum())
        print("Unimportant change:", df[kans_schade + ' unimportant change'].sum())
        print("Justified+important change:", df[kans_schade + ' justified+important change'].sum())
    