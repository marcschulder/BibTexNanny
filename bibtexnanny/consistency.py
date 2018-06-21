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
    title2duplicateEntries = nanny.findDuplicateTitles(entries)
    if title2duplicateEntries:
        print(HEADLINE_PATTERN.format("Duplicate Keys"))
        for duplicateTitle, duplicateTitleEntries in title2duplicateEntries.items():
            keysString = getEnumerationString(duplicateTitleEntries)
            firstTitle = duplicateTitleEntries[0][nanny.FIELD_TITLE]
            print("Entries {} have the same title: {}".format(keysString, firstTitle))
        print()

    # Missing fields #
    key2availability = nanny.getFieldAvailabilities(entries)
    if key2availability:
        print(HEADLINE_PATTERN.format("Missing fields"))
        for key, availability in key2availability.items():
            missingRequiredFields = availability[nanny.FIELD_IS_REQUIRED_MISSING]
            missingOptionalFields = availability[nanny.FIELD_IS_OPTIONAL_MISSING]
            # if missingRequiredFields:
            if missingRequiredFields or missingOptionalFields:
                print("Entry {}".format(key))
                if missingRequiredFields:
                    print("  Required missing: ", ', '.join(missingRequiredFields))
                if missingOptionalFields:
                    print("  Optional missing: ", ', '.join(missingOptionalFields))
        print()

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    key2unsecuredChars = nanny.findUnsecuredUppercase(entries)
    if key2unsecuredChars:
        print(HEADLINE_PATTERN.format("Titles with uppercase characters that are not secured by curly braces"))
        for key in key2unsecuredChars:
            title = entries[key][nanny.FIELD_TITLE]
            print("Entry {} has unsecured uppercase characters: {}".format(key, title))
        print()

    # Unnecessary curly braces
    print(NOT_IMPLEMENTED_PATTERN.format("unnecessary curly braces"))

    # Bad page numbers
    badPageNumberEntries = nanny.findBadPageNumbers(entries, tolerateSingleHyphens=False)
    if badPageNumberEntries:
        print(HEADLINE_PATTERN.format("Titles with badly formatted page numbers"))
        for entry in badPageNumberEntries:
            print("Entry {} has bad page number format: {}".format(entry.key, entry[nanny.FIELD_PAGES]))
        print()

    # Inconsistent Formatting #
    # Inconsistent names for conferences
    print(NOT_IMPLEMENTED_PATTERN.format("inconsistent names for conferences"))

    # Incomplete name initials formatting
    print(NOT_IMPLEMENTED_PATTERN.format("incomplete name initials formatting"))

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
