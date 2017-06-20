import pandas as pd
try:
    import ujson as js
except ImportError:
    # fallback to slower json
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

    minimal_feat = ['Denominazione in italiano','Denominazione in tedesco','Denominazione regione',
                    'Denominazione provincia',
                    'Codice Comune numerico con 107 province (dal 2006 al 2009)',
                    'Codice Comune numerico con 103 province (dal 1995 al 2005)',
                    'Codice Catastale del comune']

    df = df[minimal_feat]
    df = df.dropna(how="all")
    df = df.fillna('')
    df = df.replace(to_replace="-", value="")

    final_dict = dict()

    df_dict = df.to_dict(orient='records')

    metadata = dict()
    metadata["date"] = "18062017"
    metadata["source"] = "istat"

    final_dict["metadata"] = metadata
    final_dict["data"] = df_dict

    with io.open('../../../json_datasets/comuni/comuni_min.json', 'w', encoding='utf8') as outfile:
        data_towrite = js.dumps(final_dict, outfile, indent=4, ensure_ascii=False)
        outfile.write(unicode(data_towrite))
    

if __name__ == '__main__':
    sys.exit(main())
