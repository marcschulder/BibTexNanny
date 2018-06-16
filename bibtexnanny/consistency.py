#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Checks the consistency of BibTeX entries.
"""

import argparse

from bibtexnanny import nanny

__author__ = 'Marc Schulder'

HEADLINE_PATTERN = "===== {} ====="
NOT_IMPLEMENTED_PATTERN = "Warning for {} not yet implemented"


def getEnumerationString(entries, quotes=None):
    if len(entries) == 0:
        return ''
    if len(entries) == 1:
        if quotes is None:
            return entries[0].key
        else:
            return "{1}{0}{1}".format(entries[0].key, quotes)

    else:
        first_entry = entries[0]
        last_entry= entries[-1]
        remaining_entries = entries[1:-1]

        elems = [first_entry.key]
        for entry in remaining_entries:
            elems.append(', ')
            if quotes is not None:
                elems.append(quotes)
            elems.append(entry.key)
            if quotes is not None:
                elems.append(quotes)

        elems.append(' and ')
        if quotes is not None:
            elems.append(quotes)
        elems.append(last_entry.key)
        if quotes is not None:
            elems.append(quotes)

        return ''.join(elems)


def checkConsistency(entries):
    # Check for Duplicates #
    # Duplicate keys
    print(NOT_IMPLEMENTED_PATTERN.format("duplicate keys"))
    # duplicateKeys = nanny.findDuplicateKeys(entries)
    # if duplicateKeys:
    #     print(HEADLINE_PATTERN.format("Duplicate Keys"))
    #     for duplicateKey in duplicateKeys:
    #         print("Found duplicate key:".format(duplicateKey))
    #     print()

    # Duplicate titles
    duplicateTitles = nanny.findDuplicateTitles(entries)
    if duplicateTitles:
        print(HEADLINE_PATTERN.format("Duplicate Keys"))
        for duplicateTitle, duplicateTitleEntries in duplicateTitles.items():
            keysString = getEnumerationString(duplicateTitleEntries)
            firstTitle = duplicateTitleEntries[0]['title']
            print("Entries {} have the same title: {}".format(keysString, firstTitle))
        print()

    # Missing fields #
    # Missing mandatory fields
    print(NOT_IMPLEMENTED_PATTERN.format("missing mandatory fields"))
    # Missing optional fields
    print(NOT_IMPLEMENTED_PATTERN.format("missing optional fields"))

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    key2unsecuredChars = nanny.findUnsecuredUppercase(entries)
    if key2unsecuredChars:
        print(HEADLINE_PATTERN.format("Titles with uppercase characters that are not secured by curly braces"))
        for key in key2unsecuredChars:
            title = entries[key]['title']
            print("Entry {} has unsecured uppercase characters: {}".format(key, title))
        print()

    # Unnecessary curly braces
    print(NOT_IMPLEMENTED_PATTERN.format("unnecessary curly braces"))

    # Bad page number hyphens
    print(NOT_IMPLEMENTED_PATTERN.format("bad page number hyphens"))

    # Inconsistent Formatting #
    # Inconsistent names for conferences
    print(NOT_IMPLEMENTED_PATTERN.format("inconsistent names for conferences"))

    # Inconsistent name initials formatting
    print(NOT_IMPLEMENTED_PATTERN.format("inconsistent name initials formatting"))

    # Inconsistent location names
    print(NOT_IMPLEMENTED_PATTERN.format("inconsistent names for conferences"))


def main():
    parser = argparse.ArgumentParser(description='Check the consistency of BibTeX entries.')
    parser.add_argument('bibtexfile')
    parser.add_argument('-a', '--aux')
    # TODO: Allow multiple bibtex files
    args = parser.parse_args()

    entries = nanny.loadBibTex(args.bibtexfile)
    if args.aux:
        keyWhitelist = nanny.loadCitedKeys(args.aux)
        entries = nanny.filterEntries(entries, keyWhitelist)
    checkConsistency(entries)


if __name__ == '__main__':
    main()
