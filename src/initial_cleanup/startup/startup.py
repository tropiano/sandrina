#!/usr/bin/env python

import pandas as pd
import sys
try:
    import ujson as js
except ImportError:
    # fallback to slower json
    import json as js
from django.utils.encoding import smart_str


def main():

    df = pd.read_csv("../../../datasets/startup/startup_01052017.csv",
                     skiprows=[1,2,3,4,365,475,483,485,486],
                     delimiter='|',
                     encoding='latin-1')
    
    interesting_columns = ['denominazione', 'nat.giuridica',
                           'codice fiscale ', 'pv', 'comune',
                           'data iscrizione alla sezione delle startup',
                           'data iscrizione al Registro Imprese',
                           'data inizio dell\'esercizio effettivo dell\'attivita',
                           'ateco 2007', 'settore', 'attivita', 'sito internet',
                           'regione', 'sezione attivita', 'classe addetti',
                           'classe val.prod.', 'alto valore tecnologico',
                           'vocazione sociale', 'classe cap.sociale',
                           'spese in ricerca e sviluppo',
                           'forza lavoro con titoli ', 'possesso di brevetti ',
                           'data dichiarazione', 'prevalenza femminile ',
                           'prevalenza giovanile ', 'prevalenza straniera ']
    
    df_skim = df[df.columns[:25]]
    
    # the json output that will be imported in the DB
    output = {}
    output['metadata'] = {}
    output['metadata']['source'] = 'regione toscana'
    output['metadata']['date'] = '01052017'
    output['data'] = []
    
    for rec in range(0, len(df.index) - 1):
        entry = {}
        for col in interesting_columns:
            entry[col] = smart_str(df.iloc[rec][col]).strip(' \t\n\r')
        output['data'].append(entry)
    
    with open('../../../json_datasets/startup/startup.json', 'w') as outfile:
        js.dump(output, outfile, indent=4)


if __name__ == '__main__':                                                      
    sys.exit(main())
