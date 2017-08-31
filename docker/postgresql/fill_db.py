import psycopg2
import json as js


#load the comuni json file
f = open("/var/lib/postgresql/comuni_min.json")
js_file = f.read()
js_dict = js.loads(js_file,encoding='utf-8')
js_data=js_dict['data']


conn = psycopg2.connect("dbname='sandrina' user='sandrina' host='postgresql' password='v5sYvBKw'")
cur = conn.cursor()

for j in js_data:
    
    data_tuple = (j['Codice Catastale del comune'], j['Codice Comune numerico con 103 province (dal 1995 al 2005)'],
                  j['Codice Comune numerico con 107 province (dal 2006 al 2009)'], j['Denominazione in italiano'],
                  j['Denominazione regione'])
                  
    cur.execute("INSERT INTO comuni(codice_catastale, codice_comune_103, codice_comune_107, nome, regione) VALUES (%s,%s,%s,%s,%s)", data_tuple)
    
    
conn.commit()