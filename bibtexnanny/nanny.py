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


def findDuplicateKeys(entries):
    # Can not be checked for right now because biblib throws errors when encountering repeated keys

    raise UserWarning("Finding duplicate keys is not yet implemented.")

    # duplicates = set()
    # for entry in entries:
    #     print(entry)
    #     break
    # return duplicates


def findDuplicateTitles(entries, ignoreCurlyBraces=True, ignoreCaps=True):
    seen = {}
    for key, entry in entries.items():
        title = entry["title"]
        if ignoreCurlyBraces:
            title = title.replace('{', '')
            title = title.replace('}', '')
        if ignoreCaps:
            title = title.lower()

        seen.setdefault(title, []).append(entry)

    duplicates = {}
    for title, entries in seen.items():
        if len(entries) >= 2:
            duplicates[title] = entries

    return duplicates


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
    key2unsecuredChars = {}
    for key, entry in entries.items():
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
