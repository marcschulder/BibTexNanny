#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fixes BibTeX entries.
"""

import nanny
import argparse

__author__ = 'Marc Schulder'

HEADLINE_PATTERN = "===== {} ====="
NOT_IMPLEMENTED_PATTERN = "Warning for {} not yet implemented"


def checkConsistency(entries):
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

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    unsecuredTitles = nanny.findUnsecuredUppercase(entries)
    print(NOT_IMPLEMENTED_PATTERN.format("unsecured uppercase characters in titles"))

    # Unnecessary curly brackets
    print(NOT_IMPLEMENTED_PATTERN.format("unnecessary curly brackets"))

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
    # TODO: Allow aux file to limit fixes check to items actually cited in latex document.

    args = parser.parse_args()

    entries = nanny.loadBibTex(args.bibtexfile)
    checkConsistency(entries)


if __name__ == '__main__':
    main()
