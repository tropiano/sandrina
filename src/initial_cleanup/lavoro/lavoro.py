#!/usr/bin/env python
from django.utils.encoding import smart_str
import pandas as pd
import numpy as np
import sys
import json as js
import io 



def main():

    df = pd.read_csv("../../../datasets/Toscana_SistemiLocaliLavoro/R09_indicatori_2011_sll_readable.csv", encoding='latin-1')


    # the json output that will be imported in the DB
    output = {}
    output['metadata'] = {}
    output['metadata']['source'] = 'regione toscana'
    output['metadata']['date'] = '19062017'
    output['data'] = []

    print output

    for rec in range(0, len(df.index) - 1):
        entry = {}
        for col in df.columns:
            #print col, rec
            entry[col] = smart_str(df.iloc[rec][col]).strip(' \t\n\r')
        output['data'].append(entry)

    with io.open('../../../json_datasets/lavoro/lavoro.json', 'w', encoding='utf8') as outfile:
        data_towrite = js.dumps(output, outfile, indent=4, ensure_ascii=False)
        outfile.write(unicode(data_towrite))
      

if __name__ == '__main__':
    sys.exit(main())


