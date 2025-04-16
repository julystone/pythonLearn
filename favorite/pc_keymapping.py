# encoding: utf-8
import pandas as pd




class KeyMapping:
    def __init__(self, file_path="../ExcelFiles/key_map.xlsx"):
        self.file_path = file_path
        self.mapping =self.get_mapping(self.words_get())

    def words_get(self):
        mapping_df = pd.read_excel(self.file_path, sheet_name='id_mapping')
        mapping_df = mapping_df[['Contract_Code', 'Contract_Abbr']]
        return mapping_df

    def get_mapping(self, mapping_df) -> dict:
        mapping_df.fillna('', inplace=True)
        mapping = dict(zip(mapping_df['Contract_Abbr'], mapping_df['Contract_Code']))

        return mapping

def app():
    res = KeyMapping().mapping
    print(res)

GlobalKeyMapping = KeyMapping().mapping

if __name__ == '__main__':
    app()
    str = "FU"
    for key, value in GlobalKeyMapping.items():

        temp = str.replace(key, value)
        print(temp)