import cgi
import sqlite3
import redis
import hashlib

books = {
    '1 Corinthians': 'cor1',
    '1 John': 'john1',
    '1 Peter': 'peter1',
    '1 Thessalonians': 'thess1',
    '1 Timothy': 'tim1',
    '2 Corinthians': 'cor2',
    '2 John': 'john2',
    '2 Peter': 'peter2',
    '2 Thessalonians': 'thess2',
    '2 Timothy': 'tim2',
    '3 John': 'john3',
    'Acts': 'acts',
    'Colossians': 'col',
    'Ephesians': 'eph',
    'Galatians': 'gal',
    'Hebrews': 'heb',
    'James': 'james',
    'John': 'john',
    'Jude': 'jude',
    'Luke': 'luke',
    'Mark': 'mark',
    'Matthew': 'matthew',
    'Philemon': 'phm',
    'Phillipians': 'phil',
    'Revelation': 'revelation',
    'Romans': 'romans',
    'Titus': 'titus'
}

r = redis.Redis(host='localhost', port=6379, db=0)

"""
john:15:9 => [
    665dcf6c1ca39af1e1b96904ddf6807102976a01,
    665dcf6c1ca39af1e1b96904ddf6807102976a01
]

words:665dcf6c1ca39af1e1b96904ddf6807102976a01 => [
    "word",
    "parse",
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

    def __init__(self):
        self.connection = sqlite3.connect('nt.db')
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
                        r.rpush('%s:%d:%d' % (book_name, chapter, verse), s)
                        r.hset('word:%s' % s, 'word', word['word'])
                        r.hset('word:%s' % s, 'parse', word['parse'])
                        r.hset('word:%s' % s, 'strong', word['strong'])
        self.save_definitions()

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
            r.set('strong:%d' % number, definition)

    def unicodeToHTMLEntities(self, text):
        """
        Convert unicode to HTML entities.  For example '&' becomes '&amp;'
        """
        text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
        return text


if __name__ == '__main__':
    loader = Loader()
    loader.save_redis()
