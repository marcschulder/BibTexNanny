#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fixes BibTeX entries.
"""

from bibtexnanny import nanny
import argparse

__author__ = 'Marc Schulder'

HEADLINE_PATTERN = "===== {} ====="
NOT_IMPLEMENTED_PATTERN = "Auto-fix for {} not yet implemented"


def fixEntries(entries):
    # Check for Duplicates #
    # Duplicate keys
    print(NOT_IMPLEMENTED_PATTERN.format("duplicate keys"))

    # Duplicate titles
    duplicateTitles = nanny.findDuplicateTitles(entries)
    print(NOT_IMPLEMENTED_PATTERN.format("duplicate titles"))


    # Missing fields #
    # Missing mandatory fields
    print(NOT_IMPLEMENTED_PATTERN.format("missing mandatory fields"))
    # Missing optional fields
    print(NOT_IMPLEMENTED_PATTERN.format("missing optional fields"))
    print()

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    key2unsecuredChars = nanny.findUnsecuredUppercase(entries)
    if key2unsecuredChars:
        print(HEADLINE_PATTERN.format("Securing uppercase characters in titles with curly braces"))
        for key, unsecuredChars in key2unsecuredChars.items():
            original_title = entries[key]['title']
            fixed_title = fixUnsecuredUppercase(original_title, unsecuredChars)
            print("Fixed {} unsecured uppercase characters in entry {}".format(len(unsecuredChars), key))
            print("  Before: {}".format(original_title))
            print("  After:  {}".format(fixed_title))
            entries[key]['title'] = fixed_title
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

    return entries


def fixUnsecuredUppercase(text, unsecuredChars):
    unsecuredChars = set(unsecuredChars)
    fixed_chars = []
    lastCharWasClosingCurlyBrace=False
    for i, c in enumerate(text):
        if i in unsecuredChars:
            if lastCharWasClosingCurlyBrace:
                fixed_chars.pop(-1)
            else:
                fixed_chars.append('{')
            fixed_chars.append(c)
            fixed_chars.append('}')
            lastCharWasClosingCurlyBrace = True
        else:
            fixed_chars.append(c)
            lastCharWasClosingCurlyBrace = c == '}'
    fixed_title = ''.join(fixed_chars)
    return fixed_title


def main():
    parser = argparse.ArgumentParser(description='Check the consistency of BibTeX entries.')
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('-a', '--aux')
    # TODO: Allow aux file to limit fixes check to items actually cited in latex document.

    args = parser.parse_args()

    entries = nanny.loadBibTex(args.input)
    if args.aux:
        keyWhitelist = nanny.loadCitedKeys(args.aux)
        entries = nanny.filterEntries(entries, keyWhitelist)
    fixedEntries = fixEntries(entries)
    nanny.saveBibTex(args.output, fixedEntries)


if __name__ == '__main__':
    main()
