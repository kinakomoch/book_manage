import json
import sqlite3
import pprint

import requests

from barcode_rec import barcode_rec


def books_sql(database, table, openbd_url):
        '''
        books_sql creates a database.
        You are repeatedly required to input ISBN, which is an unique number.

        Args:
                database        : string
                table           : string
                openbd_url      : string
        '''

        conn = sqlite3.connect(database)

        cur = conn.cursor()

        # Create table
        if database is None or table is None:
                cur.execute('''CREATE TABLE {0}
                        (isbn INTEGER UNIQUE, title TEXT)'''.format(table))

        # Insert a row of data
        # while True:
        #         isbn = input('Please input the ISBN or input q: ')
        #
        #         if isbn == 'q' or isbn =='':
        #                 break
                #
                # url = openbd_url + isbn
                #
                # # isbn must be integer
                # isbn = isbn.replace('-', '')
                # isbn = int(isbn)
                #
                # req = requests.get(url)
                # data = json.loads(req.text)
                # title = data[0]['summary']['title']
                #
                # # if the same isbn is existing, skip
                # try:
                #         cur.execute("INSERT INTO books VALUES (?, ?)", [isbn, title])
                # except sqlite3.IntegrityError:
                #         continue
                #
                # cur.execute('SELECT * FROM books')
                # pprint.pprint(cur.fetchall())
                
        isbns = barcode_rec()

        for isbn in isbns:
                if isbn == '':
                        continue

                url = openbd_url + isbn
                isbn = int(isbn)

                try:
                        req = requests.get(url)
                        data = json.loads(req.text)

                        title = data[0]['summary']['title']
                except TypeError:
                        continue

                try:
                        cur.execute("INSERT INTO {0} VALUES (?, ?)".format(table), [isbn, title])
                except sqlite3.IntegrityError:
                        continue

        cur.execute('SELECT * FROM {0}'.format(table))
        pprint.pprint(cur.fetchall())

        conn.commit()
        conn.close()


if __name__ == '__main__':
        database = 'book_deals.db'
        table = 'books'
        openbd_url = 'https://api.openbd.jp/v1/get?isbn='
        books_sql(database, table, openbd_url)
