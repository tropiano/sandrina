import pandas as pd
import numpy as np


def main():

    df = pd.read_csv("../datasets/salute/osservatori_comuni.csv")

    interesting_feat = ["Produzione pro-capite Rifiuti Urbani","Reddito imponibile medio per contribuente",
                        "Numero medio componenti per famiglie","% di Raccolta Differenziata",
                        "Reddito imponibile medio per residente","Rapporto tra avviamenti/cessazioni (x 100)",
                        "Rapporto tra avviamenti/cessazioni di stranieri (x 100)",'Tasso grezzo di disoccupazione (x100)',
                        "Tasso grezzo di disoccupazione stranieri (x100)","Quoziente di incremento totale (x 1.000)",
                        "Percentuale nati di cittadinanza non italiana","Tasso di pensioni sociali e assegni sociali (x 100)",
                        "Percentuale studenti con esito negativo - secondaria II grado",
                        "Superamento dei limiti normativi dovuti a Srb: numero superamenti limite di esposizione e limite di attenzione",
                        "Superamento dei limiti normativi dovuti a impianti Rtv: numero superamenti limite di esposizione e limite di attenzione",
                        "Percentuale di avviamenti a termine","Percentuale studenti con esito negativo - secondaria I grado",
                        "Numero interventi di controllo per abitante","Tasso di famiglie che chiedono integrazione canoni di locazione (x 1000)",
                        'Percentuale studenti stranieri iscritti alle scuole secondarie di primo grado',
                        'Percentuale studenti stranieri iscritti alle scuole secondarie di secondo grado',
                       'Indice di vecchiaia (x 100)','Quoziente di incremento naturale (x 1.000)']

    df_skim = df[df.nome_indicatore.isin(interesting_feat)]

    list_comuni = df_skim.comuni.unique()

    test_list = []
    for com in list_comuni:
        for year in range(2007,2015):
            test_tuple = (com,year)
            for name in interesting_feat:
                #print name
                df_temp = df_skim[(df_skim["nome_indicatore"] == name) & (df_skim["comuni"]==com)]
                #print df_temp["2007"]
                #print df_temp.shape
                if df_temp.empty == True:
                    continue
                test_tuple = test_tuple + (df_temp.iloc[0][str(year)],)

            test_list.append(test_tuple)

    df_new = pd.DataFrame(test_list,columns=["comune","year"]+interesting_feat)

    df_new.set_value(999,'Tasso grezzo di disoccupazione (x100)',np.nan)
    df_new.set_value(280,'Produzione pro-capite Rifiuti Urbani',np.nan)
    df_new.set_value([999,1158,1159,1525,1535],'Tasso grezzo di disoccupazione stranieri (x100)',np.nan)

    df_new = df_new.fillna('')
    df_dict = df_new.to_dict(orient='records')

    metadata = dict()
    metadata["date"] = "18052017"
    metadata["source"] = "regione toscana"

    final_dict = dict()

    final_dict["metadata"] = metadata
    final_dict["data"] = df_dict

    return final_dict

if __name__ == '__main__':
    main()
