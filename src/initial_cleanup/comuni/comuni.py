import pandas as pd
import json as js
import sys
import io


def main():

    df = pd.read_csv("../../../datasets/elenco-comuni-italiani.csv", delimiter=";", encoding="latin-1")

    lista_columns = list(df.keys())

    df = df[lista_columns]
    df = df.dropna(how="all")
    df = df.fillna('')
    df = df.replace(to_replace="-", value="")

    final_dict = dict()

    df_dict = df.to_dict(orient='records')

    metadata = dict()
    metadata["date"] = "03062017"
    metadata["source"] = "istat"

    final_dict["metadata"] = metadata
    final_dict["data"] = df_dict

    with io.open('../../../json_datasets/comuni/comuni.json', 'w', encoding='utf8') as outfile:
        data_towrite = js.dumps(final_dict, outfile, indent=4, ensure_ascii=False)
        outfile.write(unicode(data_towrite))


if __name__ == '__main__':
    sys.exit(main())
