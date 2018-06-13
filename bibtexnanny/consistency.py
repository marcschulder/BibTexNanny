#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Checks the consistency of BibTeX entries.
"""

__author__ = 'Marc Schulder'

import sys
import os
import re
import argparse
import biblib.bib

HEADLINE_PATTERN = "===== {} ====="


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


def getEnumerationString(items, quotes=None):
    if len(items) == 0:
        return ''
    if len(items) == 1:
        if quotes is None:
            return items[0]
        else:
            return "{1}{0}{1}".format(items[0], quotes)

    else:
        first_item = items[0]
        last_item = items[-1]
        remaining_items = items[1:-1]

        elems = [first_item]
        for item in remaining_items:
            elems.append(', ')
            if quotes is not None:
                elems.append(quotes)
            elems.append(item)
            if quotes is not None:
                elems.append(quotes)

        elems.append(' and ')
        if quotes is not None:
            elems.append(quotes)
        elems.append(last_item)
        if quotes is not None:
            elems.append(quotes)

        return ''.join(elems)


def checkConsistency(entries):
    # Check for Duplicates #
    # Duplicate keys
    duplicateKeys = findDuplicateKeys(entries)
    if duplicateKeys:
        print(HEADLINE_PATTERN.format("Duplicate Keys"))
        for duplicateKey in duplicateKeys:
            print("Found duplicate key:".format(duplicateKey))

    # Duplicate keys
    duplicateTitles = findDuplicateTitles(entries)
    if duplicateTitles:
        print(HEADLINE_PATTERN.format("Duplicate Keys"))
        for duplicateTitle, keys in duplicateTitles.items():
            keysString = getEnumerationString(keys)
            firstTitle = entries[keys[0]]['title']
            print("Entries {} have the same title: {}".format(keysString, firstTitle))


def findDuplicateKeys(entries):
    # Can not be checked for right now because biblib throws errors when encountering repeated keys

    # duplicates = set()
    # for entry in entries:
    #     print(entry)
    #     break
    # return duplicates

    return set()


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


def main():
    parser = argparse.ArgumentParser(description='Check the consistency of BibTeX entries.')
    parser.add_argument('bibtexfile')

    args = parser.parse_args()

    entries = loadBibTex(args.bibtexfile)
    checkConsistency(entries)


if __name__ == '__main__':
    main()
