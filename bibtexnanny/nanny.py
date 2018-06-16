#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collection of functions used by various tools of the BibTexNanny toolkit.
"""

import sys
import os
import re
from collections import OrderedDict

from bibtexnanny.biblib import bib

__author__ = 'Marc Schulder'


FIELD_TITLE = 'title'
FIELD_PAGES = 'pages'

FIELD_IS_REQUIRED_AVAILABLE = 'required available'
FIELD_IS_REQUIRED_MISSING = 'required missing'
FIELD_IS_OPTIONAL_AVAILABLE = 'optional available'
FIELD_IS_OPTIONAL_MISSING = 'optional missing'
FIELD_IS_ADDITIONAL = 'additional'

# TYPES = ['article', 'book', 'booklet', 'conference', 'inbook', 'incollection', 'inproceedings', 'manual',
#          'mastersthesis', 'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished']


# TYPE2REQUIRED_FIELDS = {'article': (('author',), ('title',), ('journal',), ('year',), ('volume',)),
#                         'book': (('author', 'editor'), ('title',), ('publisher',), ('year',)),
#                         'booklet': (('title',),),
#                         'conference': (('author',), ('title',), ('booktitle',), ('year',)),
#                         'inbook': (('author', 'editor'), ('title',), ('chapter', 'pages'), ('publisher',), ('year',)),
#                         'incollection': (('author',), ('title',), ('booktitle',), ('publisher',), ('year',)),
#                         'inproceedings': (('author',), ('title',), ('booktitle',), ('year',)),
#                         'manual': (('title',),),
#                         'mastersthesis': (('author',), ('title',), ('school',), ('year',)),
#                         'misc': (),
#                         'phdthesis': (('author',), ('title',), ('school',), ('year',)),
#                         'proceedings': (('title',), ('year',)),
#                         'techreport': (('author',), ('title',), ('institution',), ('year',)),
#                         'unpublished': (('author',), ('title',), ('note',)),
#                         }
TYPE2REQUIRED_FIELDS = {'article': {'author', 'title', 'journal', 'year', 'volume'},
                        'book': {'author', 'editor', 'title', 'publisher', 'year'},
                        'booklet': {'title'},
                        'conference': {'author', 'title', 'booktitle', 'year'},
                        'inbook': {'author', 'editor', 'title', 'chapter', 'pages', 'publisher', 'year'},
                        'incollection': {'author', 'title', 'booktitle', 'publisher', 'year'},
                        'inproceedings': {'author', 'title', 'booktitle', 'year'},
                        'manual': {'title'},
                        'mastersthesis': {'author', 'title', 'school', 'year'},
                        'misc': {},
                        'phdthesis': {'author', 'title', 'school', 'year'},
                        'proceedings': {'title', 'year'},
                        'techreport': {'author', 'title', 'institution', 'year'},
                        'unpublished': {'author', 'title', 'note'},
                        }
TYPE2REQUIRED_ALTERNATIVES = {'book': {'author': 'editor', 'editor': 'author'},
                              'inbook': {'author': 'editor', 'editor': 'author',
                                         'chapter': 'pages', 'pages': 'chapter'},
                              }

# TYPE2OPTIONAL_FIELDS = {'article': (('number',), ('pages',), ('month',), ('note',), ('key',)),
#                         'book': (('volume', 'number'), ('series',), ('address',), ('edition',), ('month',), ('note',),
#                                  ('key',), ('url',)),
#                         'booklet': (('author',), ('howpublished',), ('address',), ('month',), ('year',), ('note',),
#                                     ('key',)),
#                         'conference': (('editor',), ('volume', 'number'), ('series',), ('pages',), ('address',),
#                                        ('month',), ('organization',), ('publisher',), ('note',), ('key',)),
#                         'inbook': (('volume', 'number'), ('series',), ('type',), ('address',), ('edition',), ('month',),
#                                    ('note',), ('key',)),
#                         'incollection': (('editor',), ('volume', 'number'), ('series',), ('type',), ('chapter',),
#                                          ('pages',), ('address',), ('edition',), ('month',), ('note',), ('key',)),
#                         'inproceedings': (('editor',), ('volume', 'number'), ('series',), ('pages',), ('address',),
#                                           ('month',), ('organization',), ('publisher',), ('note',), ('key',)),
#                         'manual': (('author',), ('organization',), ('address',), ('edition',), ('month',), ('year',),
#                                    ('note',), ('key',)),
#                         'mastersthesis': (('type',), ('address',), ('month',), ('note',), ('key',)),
#                         'misc': (('author',), ('title',), ('howpublished',), ('month',), ('year',), ('note',), ('key',)),
#                         'phdthesis': (('type',), ('address',), ('month',), ('note',), ('key',)),
#                         'proceedings': (('editor',), ('volume', 'number'), ('series',), ('address',), ('month',),
#                                         ('publisher',), ('organization',), ('note',), ('key',)),
#                         'techreport': (('type',), ('number',), ('address',), ('month',), ('note',), ('key',)),
#                         'unpublished': (('month',), ('year',), ('key',)),
#                         }
TYPE2OPTIONAL_FIELDS = {'article': {'number', 'pages', 'month', 'note', 'key'},
                        'book': {'volume', 'number', 'series', 'address', 'edition', 'month', 'note', 'key', 'url'},
                        'booklet': {'author', 'howpublished', 'address', 'month', 'year', 'note', 'key'},
                        'conference': {'editor', 'volume', 'number', 'series', 'pages', 'address', 'month',
                                       'organization', 'publisher', 'note', 'key'},
                        'inbook': {'volume', 'number', 'series', 'type', 'address', 'edition', 'month', 'note', 'key'},
                        'incollection': {'editor', 'volume', 'number', 'series', 'type', 'chapter', 'pages', 'address',
                                         'edition', 'month', 'note', 'key'},
                        'inproceedings': {'editor', 'volume', 'number', 'series', 'pages', 'address', 'month',
                                          'organization', 'publisher', 'note', 'key'},
                        'manual': {'author', 'organization', 'address', 'edition', 'month', 'year', 'note', 'key'},
                        'mastersthesis': {'type', 'address', 'month', 'note', 'key'},
                        'misc': {'author', 'title', 'howpublished', 'month', 'year', 'note', 'key'},
                        'phdthesis': {'type', 'address', 'month', 'note', 'key'},
                        'proceedings': {'editor', 'volume', 'number', 'series', 'address', 'month', 'publisher',
                                        'organization', 'note', 'key'},
                        'techreport': {'type', 'number', 'address', 'month', 'note', 'key'},
                        'unpublished': {'month', 'year', 'key'},
                        }
TYPE2OPTIONAL_ALTERNATIVES = {'book': {'volume': 'number', 'number': 'volume'},
                              'inbook': {'volume': 'number', 'number': 'volume'},
                              'incollection': {'volume': 'number', 'number': 'volume'},
                              'inproceedings': {'volume': 'number', 'number': 'volume'},
                              'proceedings': {'volume': 'number', 'number': 'volume'},
                              }


def loadBibTex(filename, loadPreamble=False):
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        raise FileNotFoundError(filename)

    preamble = ''
    if loadPreamble:
        # Read preamble
        preamble_lines = []
        with open(filename) as f:
            for line in f:
                if line.strip().startswith('@') and not line.strip().startswith('@comment{'):
                    break
                else:
                    preamble_lines.append(line)
        preamble = ''.join(preamble_lines)

    # Parse BibTex entries
    parser = bib.Parser()
    with open(filename) as f:
        parser.parse(f, log_fp=sys.stderr)

    entries = parser.get_entries()

    # # Resolve cross-references
    # entries = biblib.bib.resolve_crossrefs(entries)

    if loadPreamble:
        return entries, preamble
    else:
        return entries


def saveBibTex(filename, key2entry, preamble='', month_to_macro=True, wrap_width=70, bibdesk_compatible=False):
    entryStrings = [entry.to_bib(month_to_macro=month_to_macro, wrap_width=wrap_width,
                                 bibdesk_compatible=bibdesk_compatible) for entry in key2entry.values()]
    text = '\n\n'.join(entryStrings)
    with open(filename, 'w') as w:
        w.write(preamble)
        w.write(text)
        w.write('\n')


def loadCitedKeys(filename, lowercaseKeys=False):
    citationRE = re.compile(r"^\\citation{(.*)}$")
    keys = set()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            citationMatch = citationRE.match(line)
            if citationMatch:
                citationString = citationMatch.group(1)
                citations = citationString.split(',')
                for citation in citations:
                    if lowercaseKeys:
                        citation = citation.lower()
                    keys.add(citation)
    return keys


def filterEntries(key2entry, keyWhitelist):
    keyWhitelist = set(keyWhitelist)
    filteredEntries = OrderedDict()

    for key, entry in key2entry.items():
        key = key.lower()
        if key in keyWhitelist:
            filteredEntries[key] = entry

    return filteredEntries


def getFieldAvailability(entry):
    availability = {FIELD_IS_REQUIRED_AVAILABLE: [],
                    FIELD_IS_REQUIRED_MISSING: [],
                    FIELD_IS_OPTIONAL_AVAILABLE: [],
                    FIELD_IS_OPTIONAL_MISSING: [],
                    FIELD_IS_ADDITIONAL: [],
                    }
    unseenRequiredFields = set(TYPE2REQUIRED_FIELDS[entry.typ])
    requiredFields = TYPE2REQUIRED_FIELDS[entry.typ]
    unseenOptionalFields = set(TYPE2OPTIONAL_FIELDS[entry.typ])
    optionalFields = TYPE2OPTIONAL_FIELDS[entry.typ]
    requiredAlts = TYPE2REQUIRED_ALTERNATIVES.get(entry.typ, {})
    optionalAlts = TYPE2OPTIONAL_ALTERNATIVES.get(entry.typ, {})

    for field in entry:
        if field in requiredFields:
            availability[FIELD_IS_REQUIRED_AVAILABLE].append(field)
            unseenRequiredFields.discard(field)
            if field in requiredAlts:
                unseenRequiredFields.discard(requiredAlts[field])
        elif field in optionalFields:
            availability[FIELD_IS_OPTIONAL_AVAILABLE].append(field)
            unseenOptionalFields.discard(field)
            if field in optionalAlts:
                unseenOptionalFields.discard(optionalAlts[field])
        else:
            availability[FIELD_IS_ADDITIONAL].append(field)
    availability[FIELD_IS_REQUIRED_MISSING].extend(unseenRequiredFields)
    availability[FIELD_IS_OPTIONAL_MISSING].extend(unseenOptionalFields)

    return availability


def getFieldAvailabilities(entries):
    key2availability = OrderedDict()
    for key, entry in entries.items():
        key2availability[key] = getFieldAvailability(entry)
    return key2availability


def findDuplicateKeys(entries):
    # Can not be checked for right now because biblib throws errors when encountering repeated keys

    raise UserWarning("Finding duplicate keys is not yet implemented.")

    # duplicates = set()
    # for entry in entries:
    #     print(entry)
    #     break
    # return duplicates


def findDuplicateTitles(entries, ignoreCurlyBraces=True, ignoreCaps=True):
    key2seen = {}
    for key, entry in entries.items():
        title = entry["title"]
        if ignoreCurlyBraces:
            title = title.replace('{', '')
            title = title.replace('}', '')
        if ignoreCaps:
            title = title.lower()

        key2seen.setdefault(title, []).append(entry)

    key2duplicates = {}
    for title, entries in key2seen.items():
        if len(entries) >= 2:
            key2duplicates[title] = entries

    return key2duplicates


def findUnsecuredUppercase(entries):
    """
    Find entries that contain uppercase characters that are not secured by curly braces.
    The only uppercase character that needs no braces is the first letter of the title, as it is automatically
    converted to uppercase anyway.

    Background: In most bibliography styles titles are by defauly displayed with only the first character being
    uppercase and all others are forced to be lowercase. If you want to display any other uppercase characters, you
    have to secure them by wrapping them in curly braces.
    :param entries:
    :return:
    """
    key2unsecuredChars = OrderedDict()
    for key, entry in entries.items():
        if "title" not in entry:
            continue

        title = entry["title"]
        isSecured = False

        # Skip first character (unless it is a curly brace) as it is auto-converted to uppercase anyway
        i_start = 0
        if title[0] != '{':
            title = title[1:]
            i_start = 1

        for i, c in enumerate(title, start=i_start):
            if c == '{':
                isSecured = True
            elif c == '}':
                isSecured = False
            elif not isSecured and c.isupper():
                key2unsecuredChars.setdefault(key, []).append(i)
    return key2unsecuredChars


def findBadPageNumbers(entries, tolerateSingleHyphens=True):
    if tolerateSingleHyphens:
        pageRE = re.compile(r'^{0}(,{0})*$'.format(r'\d+((\-\-\d+)|(\-\d+)|(\+))?'))
    else:
        pageRE = re.compile(r'^{0}(,{0})*$'.format(r'\d+((\-\-\d+)|(\+))?'))

    badEntries = []
    for key, entry in entries.items():
        if "pages" not in entry:
            continue

        pages = entry["pages"]
        if not pageRE.match(pages):
            badEntries.append(entry)
    return badEntries
