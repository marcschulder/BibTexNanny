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
        for duplicateTitle, keys in duplicateTitles.items():
            keysString = getEnumerationString(keys)
            firstTitle = entries[keys[0]]['title']
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
    # TODO: Allow multiple bibtex files
    # TODO: Allow aux file to limit consistency check to items actually cited in latex document.

    args = parser.parse_args()

    entries = nanny.loadBibTex(args.bibtexfile)
    checkConsistency(entries)


if __name__ == '__main__':
    main()
