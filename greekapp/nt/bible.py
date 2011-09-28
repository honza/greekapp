import redis

"""
  All Greek verbs are listed in one of three various forms:

       1) V-tense-voice-mood
       2) V-tense-voice-mood-person-number
       3) V-tense-voice-mood-case-number-gender


  DECLINED FORMS:

    All follow the order: prefix-case-number-gender-(suffix)
"""

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

indeclinable = {
     'ADV'   : 'Adverb or adverb and particle combined',
     'CONJ'  : 'Conjunction or conjunctive particle',
     'COND'  : 'Conditional particle or conjunction',
     'PRT'   : 'Particle, disjunctive particle',
     'PREP'  : 'Preposition',
     'INJ'   : 'Interjection',
     'ARAM'  : 'AraMaic transliterated word (indeclinable)',
     'HEB'   : 'Hebrew transliterated word (indeclinable)',
     'N-PRI' : 'Indeclinable Proper Noun',
     'A-NUI' : 'Indeclinable Numeral (Adjective)',
     'N-LI'  : 'Indeclinable Letter (Noun)',
     'N-OI'  : 'Indeclinable Noun of Other type'
}

declinable = {
    'N':'Noun',
    'A':'Adjective',
    'R':'Relative pronoun',
    'C':'Reciprocal pronoun',
    'D':'Demonstrative pronoun',
    'T':'Definite article',
    'K':'Correlative pronoun',
    'I':'Interrogative pronoun',
    'X':'Indefinite pronoun',
    'Q':'Correlative or interrogative pronoun',
    'F':'ReFlexive pronoun (person 1,2,3 added)',
    'S':'Possessive pronoun (person 1,2,3 added)',
    'P':'Personal pronoun (person 1,2,3 added) (Note: 1st and 2nd personal pronouns have no gender)'
}

cases = {
   'N': 'Nominative',
   'V': 'Vocative',
   'G': 'Genitive',
   'D': 'Dative',
   'A': 'Accusative'
}

numbers = {
    'S': 'Singular',
    'P': 'Plural'
}

genders = {
    'M': 'Masculine',
    'F': 'Feminine',
    'N': 'Neuter'
}


suffixes = {
    '-S'  : 'Superlative (used primarily with adjectives and some adverbs)',
    '-C'  : 'Comparative (used primarily with adjectives and some adverbs)',
    '-ABB': 'Abbreviated form (used only with the number 666)',
    '-I'  : 'Interrogative',
    '-N'  : 'Negative (used with some particles, adverbs, adjectives, and conjunctions)',
    '-K'  : '"Kai" (CONJ), second person personal pronoun "su", or neuter definite article "to" merged by crasis with a second word; declension is that of the second word.',
    '-ATT': 'Attic Greek form'
}


tenses = {
   'P': 'Present',
   'I': 'Imperfect',
   'F': 'Future',
   '2F': 'Second Future',
   'A': 'Aorist',
   '2A': 'Second Aorist',
   'R': 'Perfect',
   '2R': 'Second perfect',
   'L': 'Pluperfect',
   '2L': 'Second Pluperfect'
}

voices = {
    'A': 'Active',
    'M': 'Middle',
    'P': 'Passive',
    'E': 'Either middle or passive',
    'D': 'Middle deponent',
    'O': 'Passive deponent',
    'N': 'Middle or passive deponent'
}

moods = {
    'I': 'Indicative',
    'S': 'Subjunctive',
    'O': 'Optative',
    'M': 'Imperative',
    'N': 'Infinitive',
    'P': 'Participle'
}

persons =  {
    '1': 'First',
    '2': 'Second',
    '3': 'Third'
}


class Bible(object):

    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def get_verse(self, book, chapter, verse):
        reference = "%s:%d:%d" % (book, int(chapter), int(verse))
        final = []
        words = self.client.lrange(reference, 0, 200)
        for w in words:
            data = self.client.hgetall('word:%s' % w)
            final.append(self.parse_word(data))
        return final

    def parse_word(self, word):
        parse = word['parse'].split('-')
        data = {}

        if parse[0] in indeclinable.keys():
            data['type'] = indeclinable[parse[0]]
        elif parse[0] in declinable.keys():
            data['type'] = declinable[parse[0]]
            case = parse[1][0]
            number = parse[1][1]
            if case in ['1', '2', '3']:
                data['person'] = parse[1][0]
                case = parse[1][1]
                number = parse[1][2]
            data['case'] = cases[case]
            data['number'] = numbers[number]
            try:
                data['gender'] = genders[parse[1][2]]
            except KeyError:
                data['gender'] = None
        else:
            data['type'] = 'Verb'
            data['tense'] = tenses[parse[1][0]]
            data['voice'] = voices[parse[1][1]]
            data['mood'] = moods[parse[1][2]]

            try:
                person = int(parse[2][0])
            except ValueError:
                person = parse[2][0]

            if isinstance(person, int):
                data['person'] = parse[2][0]
            else:
                data['case'] = cases[person]

            data['number'] = parse[2][1]

            # TODO: Test with a verse that has gerongives
            try:
                data['gender'] = parse[2][2]
            except IndexError:
                pass

        return {
            'strong': word['strong'],
            'word': word['word'],
            'parse': data
        }
