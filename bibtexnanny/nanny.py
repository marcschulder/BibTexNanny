#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collection of functions used by various tools of the BibTexNanny toolkit.
"""

__author__ = 'Marc Schulder'

import sys
import os
import re
import biblib.bib


def loadBibTex(filename):
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        raise FileNotFoundError(filename)

    parser = biblib.bib.Parser()
    with open(filename) as f:
        parser.parse(f, log_fp=sys.stderr)

    entries = parser.get_entries()

    # # Resolve cross-references
    # entries = biblib.bib.resolve_crossrefs(entries)

    return entries


def findDuplicateKeys(entries):
    # Can not be checked for right now because biblib throws errors when encountering repeated keys

    raise UserWarning("Finding duplicate keys is not yet implemented.")

    # duplicates = set()
    # for entry in entries:
    #     print(entry)
    #     break
    # return duplicates


def findDuplicateTitles(entries, ignoreCurlyBrackets=True, ignoreCaps=True):
    seen = {}
    for key, entry in entries.items():
        title = entry["title"]
        if ignoreCurlyBrackets:
            title = title.replace('{', '')
            title = title.replace('}', '')
        if ignoreCaps:
            title = title.lower()

        seen.setdefault(title, []).append(key)

    duplicates = {}
    for title, keys in seen.items():
        if len(keys) >= 2:
            duplicates[title] = keys

    return duplicates


def findUnsecuredUppercase(entries):
    """
    Find entries that contain uppercase characters that are not secured by {}-brackets.
    The only uppercase character that needs no brackets is the first letter of the title, as it is automatically
    converted to uppercase anyway.

    Background: In most bibliography styles titles are by defauly displayed with only the first character being
    uppercase and all others are forced to be lowercase. If you want to display any other uppercase characters, you
    have to secure them by wrapping them in {}-brackets.
    :param entries:
    :return:
    """
    unsecured = []
    for key, entry in entries.items():
        title = entry["title"]
        isSecured = False

        # Skip first character (unless it is a curly bracket) as it is auto-converted to uppercase anyway
        if title[0] != '{':
            title = title[1:]

        for c in title:
            if c == '{':
                isSecured = True
            elif c == '}':
                isSecured = False
            elif not isSecured and c.isupper():
                unsecured.append(key)
                break
    return unsecured
