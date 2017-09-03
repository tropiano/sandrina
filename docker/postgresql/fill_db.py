import psycopg2
import json as js


# load the comuni json file
f = open("/var/lib/postgresql/comuni_min.json")
js_file = f.read()
js_dict = js.loads(js_file, encoding='utf-8')
js_data = js_dict['data']


conn = psycopg2.connect("dbname='sandrina' user='sandrina' host='postgresql' password='v5sYvBKw'")

cur = conn.cursor()

id_comune_dict = {}

for j in js_data:

    data_tuple = (j['Codice Comune numerico con 107 province (dal 2006 al 2009)'],
                  j['Codice Catastale del comune'], j['Codice Comune numerico con 103 province (dal 1995 al 2005)'],
                  j['Codice Comune numerico con 107 province (dal 2006 al 2009)'], j['Denominazione in italiano'],
                  j['Denominazione regione'])

    # build dict id comune
    id_comune_dict[j['Denominazione in italiano']] = j['Codice Comune numerico con 107 province (dal 2006 al 2009)']

    cur.execute("INSERT INTO comuni(id, codice_catastale, codice_comune_103, codice_comune_107, nome, regione) VALUES (%s,%s,%s,%s,%s,%s)", data_tuple)

# load the salute json file
f = open("/var/lib/postgresql/salute.json")
js_file = f.read()
js_dict = js.loads(js_file, encoding='utf-8')
js_data = js_dict['data']

for j in js_data:

    try:
        comune_id = id_comune_dict[j['comune']]
        data_tuple = (comune_id, j['year'], js.dumps(j))

        cur.execute("INSERT INTO salute(comune_id, anno, entry) VALUES (%s,%s,%s)", data_tuple)
    except:
        print j['comune'], " not found"
        continue
conn.commit()
