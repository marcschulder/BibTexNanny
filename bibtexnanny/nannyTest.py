import sys
from unittest import TestCase

from bibtexnanny import nanny
from bibtexnanny.biblib import bib


TYPEFIELD = '@type'
DEFAULT_KEY_START = 'foobar'
DEFAULT_KEY = '{}{}'.format(DEFAULT_KEY_START, 2018)


def parse(text):
    parser = bib.Parser()
    parser.parse(text, log_fp=sys.stderr)
    return parser.get_entries()


def getStringEntries(field2valueyDicts, keyStart=DEFAULT_KEY_START):
    entries = [getStringEntry(field2value,
                              key='{}{}'.format(keyStart, i)) for i, field2value in enumerate(field2valueyDicts)]
    return '\n\n'.join(entries)


def getStringEntry(field2value, key=DEFAULT_KEY):
    entryPattern = '@{type}{{{key},\n{fields}}}'
    fieldPattern = '	{field} = {{{value}}},'

    entryType = field2value.get(TYPEFIELD, 'incollection')
    fieldLines = []
    for field, value in field2value.items():
        if field != TYPEFIELD:
            fieldLine = fieldPattern.format(field=field, value=value)
            fieldLines.append(fieldLine)
    entry = entryPattern.format(type=entryType, key=key, fields='\n'.join(fieldLines))
    return entry


class TestFindDuplicateTitles(TestCase):
    def test_findDuplicateTitles_Identical(self):
        title = 'Towards a new test environment'
        entryString = getStringEntries([{'Title': title},
                                        {'Title': title},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Lowercase(self):
        title = 'Towards a New Test Environment'
        entryString = getStringEntries([{'Title': title},
                                        {'Title': title.lower()},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Braces(self):
        title = 'Towards a {N}ew {T}est {E}nvironment'
        unbraced_title = title.replace('{', '').replace('}', '')
        entryString = getStringEntries([{'Title': unbraced_title},
                                        {'Title': title},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {unbraced_title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Braces2(self):
        title = 'Towards a {N}ew {T}est {E}nvironment'
        unbraced_title = title.replace('{', '').replace('}', '')
        entryString = getStringEntries([{'Title': title},
                                        {'Title': unbraced_title},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {unbraced_title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_BracesAndLowercase(self):
        title = 'Towards a {N}ew {T}est {E}nvironment'
        unbraced_title = title.replace('{', '').replace('}', '')
        entryString = getStringEntries([{'Title': unbraced_title},
                                        {'Title': title},
                                        {'Title': unbraced_title.lower()},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(3)]
        goldTitle2keys = {unbraced_title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Spaces(self):
        title = 'Towards a new test environment'
        entryString = getStringEntries([{'Title': title},
                                        {'Title': 'Towards a new   test environment'},
                                        {'Title': 'Towards a new test environment '},
                                        {'Title': '  Towards a new test environment'},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(4)]
        goldTitle2keys = {title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)


class TestFindUnsecuredUppercase(TestCase):
    def test_findUnsecuredUppercase_Basic(self):
        entryString = getStringEntry({'Title': 'Logic and Conversation'})
        key2goldChars = {DEFAULT_KEY: [10]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString))
        self.assertEqual(key2unsecuredChars, key2goldChars)

    def test_findUnsecuredUppercase_InWord(self):
        entryString = getStringEntry({'Title': 'Aligning {G}ermaNet {S}enses'})
        key2goldChars = {DEFAULT_KEY: [16]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString))
        self.assertEqual(key2unsecuredChars, key2goldChars)

    def test_findUnsecuredUppercase_AllUpper(self):
        entryString = getStringEntry({'Title': 'WORD ASSOCIATION'})
        key2goldChars = {DEFAULT_KEY: [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString))
        self.assertEqual(key2unsecuredChars, key2goldChars)

    def test_findUnsecuredUppercase_AllUpperSecuredCap(self):
        entryString = getStringEntry({'Title': 'WORD {A}SSOCIATION'})
        key2goldChars = {DEFAULT_KEY: [1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString))
        self.assertEqual(key2unsecuredChars, key2goldChars)

