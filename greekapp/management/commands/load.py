import os
from django.core.management.base import BaseCommand
import cgi
import sqlite3
import redis
import hashlib


class DataPresentException(Exception):
    pass


book_order = [
    'Matthew',
    'Mark',
    'Luke',
    'John',
    'Acts',
    'Romans',
    '1 Corinthians',
    '2 Corinthians',
    'Galatians',
    'Ephesians',
    'Phillipians',
    'Colossians',
    '1 Thessalonians',
    '2 Thessalonians',
    '1 Timothy',
    '2 Timothy',
    'Titus',
    'Philemon',
    'Hebrews',
    'James',
    '1 Peter',
    '2 Peter',
    '1 John',
    '2 John',
    '3 John',
    'Jude',
    'Revelation'
]


books = {
    'Matthew': 'matthew',
    'Mark': 'mark',
    'Luke': 'luke',
    'John': 'john',
    'Acts': 'acts',
    'Romans': 'romans',
    '1 Corinthians': 'cor1',
    '2 Corinthians': 'cor2',
    'Galatians': 'gal',
    'Ephesians': 'eph',
    'Phillipians': 'phil',
    'Colossians': 'col',
    '1 Thessalonians': 'thess1',
    '2 Thessalonians': 'thess2',
    '1 Timothy': 'tim1',
    '2 Timothy': 'tim2',
    'Titus': 'titus',
    'Philemon': 'phm',
    'Hebrews': 'heb',
    'James': 'james',
    '1 Peter': 'peter1',
    '2 Peter': 'peter2',
    '1 John': 'john1',
    '2 John': 'john2',
    '3 John': 'john3',
    'Jude': 'jude',
    'Revelation': 'revelation'
}


abbr2full = {
    'cor1': '1 Corinthians',
    'john1': '1 John',
    'peter1': '1 Peter',
    'thess1': '1 Thessalonians',
    'tim1': '1 Timothy',
    'cor2': '2 Corinthians',
    'john2': '2 John',
    'peter2': '2 Peter',
    'thess2': '2 Thessalonians',
    'tim2': '2 Timothy',
    'john3': '3 John',
    'acts': 'Acts',
    'col': 'Colossians',
    'eph': 'Ephesians',
    'gal': 'Galatians',
    'heb': 'Hebrews',
    'james': 'James',
    'john': 'John',
    'jude': 'Jude',
    'luke': 'Luke',
    'mark': 'Mark',
    'matthew': 'Matthew',
    'phm': 'Philemon',
    'phil': 'Phillipians',
    'revelation': 'Revelation',
    'romans': 'Romans',
    'titus': 'Titus'
}


"""
john:15:9 => [
    665dcf6c1ca39af1e1b96904ddf6807102976a01:
    665dcf6c1ca39af1e1b96904ddf6807102976a01
]

words:665dcf6c1ca39af1e1b96904ddf6807102976a01 => [
    "word":
    "parse":
    "strong"
]

strong:123 =>
'a beach'
"""


class Loader(object):
    """
    The greek data is in a sqlite3 database. This class can read it and parse
    it. It also knows how to talk to Redis and give it all that data.
    """

    def __init__(self, path):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

        # Do a test look up to see if there is any data
        test = self.client.lrange('john:15:9', 0, 100)
        if test:
            raise DataPresentException

        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.passage = ''
        self.data = {}
        self.shas = {}

    def save_redis(self):
        """
        Take all book data in self.data and save it in Redis
        *Note*: It doesn't save strongs yet
        """
        self.all_books()
        for book in self.data.keys():
            book_name = book
            book = self.data[book]
            for chapter in book.keys():
                for verse in book[chapter].keys():
                    print "%s %d %d" % (book_name, chapter, verse)
                    for word in book[chapter][verse]:
                        s = hashlib.sha1(word['word']).hexdigest()
                        if s not in self.shas.keys():
                            self.shas[s] = 0
                        else:
                            self.shas[s] += 1
                        self.client.rpush('%s:%d:%d' % (book_name, chapter, verse), s)
                        self.client.hset('word:%s' % s, 'word', word['word'])
                        self.client.hset('word:%s' % s, 'parse', word['parse'])
                        self.client.hset('word:%s' % s, 'strong', word['strong'])
        self.save_definitions()
        self.client.set('requests', 0)

    def all_books(self):
        """
        Load all books
        """
        keys = books.keys()
        for k in keys:
            self.get_book(k)

    def get_book(self, book):
        """
        Load, parse and save book data in self.data
        """
        book = books[book]
        m = self.cursor.execute('select * from ' + book)
        self.data[book] = {}
        for v in m:
            ch = v[0]
            ver = v[1]
            word = v[2]

            if ch not in self.data[book]:
                self.data[book][ch] = {}

            if ver not in self.data[book][ch]:
                self.data[book][ch][ver] = []

            self.data[book][ch][ver].append({
                #'word': word,
                'word': self.unicodeToHTMLEntities(word),
                'strong': v[4],
                'parse': v[3]
            })

    def get_definition(self, number):
        t = (number,)
        m = self.cursor.execute('select * from strong where number=?', t)
        for a in m:
            return a[1]

    def save_definitions(self):
        strongs = self.cursor.execute('select * from strong')
        for s in strongs:
            number = s[0]
            definition = s[1].replace('\n', '')
            print number
            self.client.set('strong:%d' % number, definition)

    def unicodeToHTMLEntities(self, text):
        """
        Convert unicode to HTML entities.  For example '&' becomes '&amp;'
        """
        text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
        return text

    def print_structure(self):
        self.all_books()

        res = {}

        for book in self.data.keys():

            chapters = []


            for i in range(1, len(self.data[book].keys()) + 1):
                verses = [x for x in self.data[book][i].keys()]
                chapters.append({
                    'number': i,
                    'verses': verses
                })


            res[abbr2full[book]] = {
                'chapters': chapters,
                'full': abbr2full[book],
                'abbr': book
            }


        final = []

        for book in book_order:
            final.append(res[book])

        import json
        print json.dumps(final, indent=4)



class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                'nt.db')
        if not path:
            self.stderr.write("Couldn't find library file.")

        try:
            loader = Loader(path)
            loader.save_redis()
        except DataPresentException:
            self.stderr.write('There is data in redis already!\n')
            return
        self.stdout.write('It worked.\n')
