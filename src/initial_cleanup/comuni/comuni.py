import pandas as pd
import json as js
import sys


def main():

    df = pd.read_csv("../../../datasets/elenco-comuni-italiani.csv", delimiter=";", encoding="latin-1")

    lista_columns = list(df.keys())

    df = df[lista_columns]
    df = df.dropna(how="all")
    df = df.fillna('')
    df = df.replace(to_replace="-", value="")

    df_dict = df.to_dict(orient='records')

    metadata = dict()
    metadata["date"] = "03062017"
    metadata["source"] = "istat"

    final_dict = dict()
    final_dict["metadata"] = metadata
    final_dict["data"] = df_dict

    with open('../../../json_datasets/comuni/comuni.json', 'w') as outfile:
        js.dump(final_dict, outfile, indent=4)


if __name__ == '__main__':
    sys.exit(main())
