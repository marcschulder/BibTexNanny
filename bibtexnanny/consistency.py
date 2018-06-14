#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Checks the consistency of BibTeX entries.
"""

__author__ = 'Marc Schulder'

import nanny
import argparse

HEADLINE_PATTERN = "===== {} ====="


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
    print("Detecting duplicate keys not yet implemented")
    # duplicateKeys = nanny.findDuplicateKeys(entries)
    # if duplicateKeys:
    #     print(HEADLINE_PATTERN.format("Duplicate Keys"))
    #     for duplicateKey in duplicateKeys:
    #         print("Found duplicate key:".format(duplicateKey))
    #     print()

    # Duplicate keys
    duplicateTitles = nanny.findDuplicateTitles(entries)
    if duplicateTitles:
        print(HEADLINE_PATTERN.format("Duplicate Keys"))
        for duplicateTitle, keys in duplicateTitles.items():
            keysString = getEnumerationString(keys)
            firstTitle = entries[keys[0]]['title']
            print("Entries {} have the same title: {}".format(keysString, firstTitle))
        print()

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    unsecuredTitles = nanny.findUnsecuredUppercase(entries)
    if unsecuredTitles:
        print(HEADLINE_PATTERN.format("Titles with uppercase characters that are not secured by curly brackets"))
        for key in unsecuredTitles:
            title = entries[key]['title']
            print("Entry {} have unsecured uppercase characters: {}".format(key, title))
        print()




def main():
    parser = argparse.ArgumentParser(description='Check the consistency of BibTeX entries.')
    parser.add_argument('bibtexfile')

    args = parser.parse_args()

    entries = nanny.loadBibTex(args.bibtexfile)
    checkConsistency(entries)


if __name__ == '__main__':
    main()
