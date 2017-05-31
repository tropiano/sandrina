import pandas as pd
import json as js
import sys


def main():

    df = pd.read_excel("../../../datasets/elenco-comuni-italiani_variazioni_al_23_aprile_2016.xls")

    lista_columns = list(df.keys())
    new_lista_columns = lista_columns[5:7] + lista_columns[9:10] + lista_columns[11:12]

    df = df[new_lista_columns]
    df = df.dropna(how="all")
    df = df.fillna('')
    df = df.replace(to_replace="-", value="")
    df = df.drop(df.index[[7999]])
    df_dict = df.to_dict(orient='records')

    metadata = dict()
    metadata["date"] = "26052017"
    metadata["source"] = "istat"

    final_dict = dict()
    final_dict["metadata"] = metadata
    final_dict["data"] = df_dict

    with open('../../../json_datasets/comuni/comuni.json', 'w') as outfile:
        js.dump(final_dict, outfile, indent=4)


if __name__ == '__main__':
    sys.exit(main())
