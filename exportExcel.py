from Mongo_Client import Mongo_Client
import pandas as pd
import xlsxwriter


class ExportExcel():
    def __init__(self):
        self.client = Mongo_Client()

    def export(self):
        collectionlist = ['Country','CountryTrend']
        for collection_name in collectionlist:
            collection = self.client.db[collection_name]
            data = pd.DataFrame(list(collection.find()))
            del data['_id']

            data.to_excel(collection_name+'.xlsx',
                          sheet_name='sheet1', index=False, engine='xlsxwriter')




if __name__ == "__main__":
    ee = ExportExcel()
    ee.export()

