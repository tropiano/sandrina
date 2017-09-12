#!/usr/bin/env python

import sys
import argparse
import psycopg2
import psycopg2.extras
import json as js
import datetime

PG_DB = "sandrina"
PG_USER = "sandrina_rw"
PG_HOST = "postgresql"
PG_PSWD = "v5sYvBKw"
PG_PORT = "5432"


class DbLoader:

    def __init__(self, file=None, table=None):
        if file is None or table is None:
            print "\n ERROR: table and file must be specified\n"
        self.file = file
        self.table = table
        self.pg_conn()

    def pg_conn(self):
        try:
            conn = psycopg2.connect(
                dbname=PG_DB,
                user=PG_USER,
                host=PG_HOST,
                password=PG_PSWD,
                port=PG_PORT)
        except:
            print "ERROR: unable to connect to the db"
            sys.exit(1)
        self.conn = conn

    def check_pivot(self):
        """
        this method check if pivot table has been deployed
        for first
        """
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT count(*) as count FROM comuni")
        if cur.fetchone()['count'] == 0:
            return False

        return True

    def load_table(self):
        try:
            f = open(self.file)
            js_file = f.read()
            js_dict = js.loads(js_file, encoding='utf-8')
            js_data = js_dict['data']
        except:
            print "ERROR: unable to open file %s" % self.file

        if self.table == "comuni":
            cur = self.conn.cursor()
            for j in js_data:

                data_tuple = ()
                data_tuple += (j['Codice Comune numerico con 107 province (dal 2006 al 2009)'],)
                data_tuple += (j['Codice Catastale del comune'],)
                data_tuple += (j['Codice Comune numerico con 103 province (dal 1995 al 2005)'],)
                data_tuple += (j['Codice Comune numerico con 107 province (dal 2006 al 2009)'],)
                data_tuple += (j['Denominazione in italiano'],)
                data_tuple += (j['Denominazione regione'],)

                INSERT_SQL = """
                INSERT INTO comuni(id,
                                   codice_catastale,
                                   codice_comune_103,
                                   codice_comune_107,
                                   nome,
                                   regione)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """
                try:
                    cur.execute(INSERT_SQL, data_tuple)
                except psycopg2.DataError:
                    warn_msg = "WARNING: the following tuple has not been inserted " + \
                          "because does not match table DDL:"
                    print warn_msg
                    print data_tuple

            try:
                self.conn.commit()
            except psycopg2.InternalError:
                print "ERROR: transaction is not committed due to unmatched records"
            cur.close()
            self.conn.close()
        elif self.table == "salute":
            self.check_pivot()

            INSERT_SQL = """
            INSERT INTO salute(comune_id, anno, entry)
                VALUES (%s,%s,%s)
            """

            cur = self.conn.cursor()
            for j in js_data:

                data_tuple = ()
                # "'" in city names has to be escaped in SQL
                comune = j['comune'].lower()
                if "'" in comune:
                    comune = comune.replace("'", "''")
                comuni_id_query = "SELECT id FROM comuni WHERE lower(nome) = '%s'" % comune
                cur.execute(comuni_id_query)
                try:
                    comuni_id = cur.fetchone()[0]
                except TypeError:
                    err_msg = "WARNING: tuple not inserted because %s is not" % comune + \
                              " in 'comuni'"
                    print err_msg
                    continue
                if comuni_id is None or comuni_id == "":
                    print "ERROR: undefined 'comuni' id for %s" % j['comune']
                    sys.exit(1)

                data_tuple += (comuni_id,)
                data_tuple += (j['year'],)
                data_tuple += (js.dumps(j),)
                try:
                    cur.execute(INSERT_SQL, data_tuple)
                except psycopg2.DataError:
                    warn_msg = "WARNING: the following tuple has not been inserted " + \
                          "because does not match table DDL:"
                    print warn_msg
                    print data_tuple

            try:
                self.conn.commit()
            except psycopg2.InternalError:
                print "ERROR: transaction is not committed due to unmatched records"
            cur.close()
            self.conn.close()
        elif self.table == "startup":
            self.check_pivot()

            INSERT_SQL = """
            INSERT INTO startup(comune_id, mese, anno, entry)
                VALUES (%s,%s,%s,%s)
            """

            cur = self.conn.cursor()
            for j in js_data:

                data_tuple = ()
                # "'" in city names has to be escaped in SQL
                comune = j['comune'].lower()
                if "'" in comune:
                    comune = comune.replace("'", "''")
                comuni_id_query = "SELECT id FROM comuni WHERE lower(nome) = '%s'" % comune
                cur.execute(comuni_id_query)
                try:
                    comuni_id = cur.fetchone()[0]
                except TypeError:
                    err_msg = "WARNING: tuple not inserted because %s is not" % comune + \
                              " in 'comuni'"
                    print err_msg
                    continue
                if comuni_id is None or comuni_id == "":
                    print "ERROR: undefined 'comuni' id for %s" % j['comune']
                    sys.exit(1)

                date = j["data inizio dell'esercizio effettivo dell'attivita"]
                mese = None
                anno = None
                if date != "":
                    datee = datetime.datetime.strptime(date, "%d/%m/%Y")
                    mese = datee.month
                    anno = datee.year

                data_tuple += (comuni_id,)
                data_tuple += (mese,)
                data_tuple += (anno,)
                data_tuple += (js.dumps(j),)
                try:
                    cur.execute(INSERT_SQL, data_tuple)
                except psycopg2.DataError:
                    warn_msg = "WARNING: the following tuple has not been inserted " + \
                          "because does not match table DDL:"
                    print warn_msg
                    print data_tuple

            try:
                self.conn.commit()
            except psycopg2.InternalError:
                print "ERROR: transaction is not committed due to unmatched records"
            cur.close()
            self.conn.close()
        elif self.table == "lavoro":
            self.check_pivot()

            INSERT_SQL = """
            INSERT INTO lavoro(comune_id, mese, anno, entry)
                VALUES (%s,%s,%s,%s)
            """

            cur = self.conn.cursor()
            for j in js_data:

                data_tuple = ()
                # "'" in city names has to be escaped in SQL
                comune = j['Denominazione del SLL 2011'].lower()
                if "'" in comune:
                    comune = comune.replace("'", "''")
                comuni_id_query = "SELECT id FROM comuni WHERE lower(nome) = '%s'" % comune
                cur.execute(comuni_id_query)
                try:
                    comuni_id = cur.fetchone()[0]
                except TypeError:
                    err_msg = "WARNING: tuple not inserted because %s is not" % comune + \
                              " in 'comuni'"
                    print err_msg
                    continue
                if comuni_id is None or comuni_id == "":
                    print "ERROR: undefined 'comuni' id for %s" % j['comune']
                    sys.exit(1)

                date = js_dict['metadata']['date']
                datee = datetime.datetime.strptime(date, "%d%m%Y")
                mese = datee.month
                anno = datee.year

                data_tuple += (comuni_id,)
                data_tuple += (mese,)
                data_tuple += (anno,)
                data_tuple += (js.dumps(j),)
                try:
                    cur.execute(INSERT_SQL, data_tuple)
                except psycopg2.DataError:
                    warn_msg = "WARNING: the following tuple has not been inserted " + \
                          "because does not match table DDL:"
                    print warn_msg
                    print data_tuple

            try:
                self.conn.commit()
            except psycopg2.InternalError:
                print "ERROR: transaction is not committed due to unmatched records"
            cur.close()
            self.conn.close()

        else:
            print "ERROR: undefined table in the db"
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("table", metavar="TABLE", help="DB table")
    parser.add_argument("file", metavar="FILE", help="file to be loaded")
    args = parser.parse_args()

    dbl = DbLoader(
        file=args.file,
        table=args.table
    )

    dbl.load_table()


if __name__ == '__main__':
    sys.exit(main())
