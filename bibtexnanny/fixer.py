#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fixes BibTeX entries.
"""

import re
import argparse

from bibtexnanny import nanny

__author__ = 'Marc Schulder'

HEADLINE_PATTERN = "===== {} ====="
NOT_IMPLEMENTED_PATTERN = "Auto-fix for {} not yet implemented"

RE_NOTPAGES_CHAR = re.compile(r'[^0-9\-+,]+')


class FixerConfig(nanny.NannyConfig):
    SECTION = 'Fixer'

    AUTOFIX = 3
    TRYFIX = 2
    PROMPTFIX = 1
    NOFIX = 0

    FALLBACK_VALUE = AUTOFIX

    CONFIGVALUE2INTERNAL = {'autofix': AUTOFIX,
                            'auto': AUTOFIX,
                            'yes': AUTOFIX,
                            'true': AUTOFIX,
                            True: AUTOFIX,
                            'tryfix': TRYFIX,
                            'try': TRYFIX,
                            'promptfix': PROMPTFIX,
                            'prompt': PROMPTFIX,
                            'nofix': NOFIX,
                            'no': NOFIX,
                            'false': NOFIX,
                            False: NOFIX,
                            }

    def _getConfigValue(self, section, key, fallback=None):
        orig_value = section.get(key, fallback=fallback)
        value = orig_value
        # print(key, value, type(value))

        if value is None:
            value = self.FALLBACK_VALUE
            print('WARNING: Config contains no information for key "{}", value defaults to "{}"'.format(
                key, self.FALLBACK_VALUE))

        if type(value) == str:
            value = value.lower()
        try:
            return self.CONFIGVALUE2INTERNAL[value]
        except KeyError:
            raise ValueError('Unknown config value: "{}"'.format(orig_value))


class FixerSilentModeConfig(nanny.NannyConfig):
    SECTION = 'Fixer Silent Mode'

    SHOW = True
    HIDE = False

    FALLBACK_VALUE = SHOW

    CONFIGVALUE2INTERNAL = {'show': SHOW,
                            'true': SHOW,
                            True: SHOW,
                            'hide': HIDE,
                            'false': HIDE,
                            False: HIDE,
                            }

    def _getConfigValue(self, section, key, fallback=None):
        orig_value = section.get(key, fallback=fallback)
        value = orig_value
        # print(key, ':', value)

        if value is None:
            value = self.FALLBACK_VALUE
            print('WARNING: Config contains no information for key "{}", value defaults to "{}"'.format(
                key, self.FALLBACK_VALUE))

        if type(value) == str:
            value = value.lower()
        try:
            return self.CONFIGVALUE2INTERNAL[value]
        except KeyError:
            raise ValueError('Unknown config value: "{}"'.format(orig_value))


class FieldInferrer:
    TYPE2INPUT2INFERRABLE = {
        'incollection':
            {('booktitle', 'year'): ('address', 'month', 'editor', 'publisher')},
        'inproceedings':
            {('booktitle', 'year'): ('address', 'month', 'editor', 'organization', 'publisher')},
    }

    def __init__(self, entries):
        self.type2input2information, self.type2input2field2conflicts = self._collectInformation(entries)
        # for typ, input2field2conflicts in self.type2input2field2conflicts.items():
        #     print(typ)
        #     for inpt, field2conflicts in input2field2conflicts.items():
        #         print('   ', inpt)
        #         for field, conflicts in field2conflicts.items():
        #             print('       ', field)
        #             for conflict in conflicts:
        #                 print('           ', conflict)

    def _collectInformation(self, entries):
        type2input2information = {}
        type2input2field2conflicts = {}

        for key, entry in entries.items():
            INPUT2INFERRABLE = self.TYPE2INPUT2INFERRABLE.get(entry.typ)
            if INPUT2INFERRABLE is not None:
                for inputFields, inferrableFields in INPUT2INFERRABLE.items():
                    inputValues = self._getAllFieldValues(entry, inputFields)

                    if inputValues is not None:
                        inferrableValueDict = self._getFieldValueDict(entry, inferrableFields)
                        if inferrableValueDict:
                            input2information = type2input2information.setdefault(entry.typ, {})
                            existingInferrableDict = input2information.get(inputValues)
                            if existingInferrableDict is not None:
                                inferrableValueDict, mergeConflictDict = self._mergeFieldValueDicts(
                                    existingInferrableDict, inferrableValueDict)
                                if mergeConflictDict:
                                    input2field2conflicts = type2input2field2conflicts.setdefault(entry.typ, {})
                                    field2conflicts = input2field2conflicts.setdefault(inputValues, {})
                                    for k, vs in mergeConflictDict.items():
                                        conflictSet = field2conflicts.setdefault(k, set())
                                        for v in vs:
                                            if v is not None:
                                                conflictSet.add(v)

                            input2information[inputValues] = inferrableValueDict

        # Clean up
        type2input2information = self.removeNoneFromDict(type2input2information)
        return type2input2information, type2input2field2conflicts

    @staticmethod
    def _getAllFieldValues(entry, fields):
        fieldValueTuples = []
        for field in fields:
            value = entry.get(field)
            if value is None:
                return None
            else:
                fieldValueTuples.append((field, value))
        return tuple(fieldValueTuples)

    @staticmethod
    def _getFieldValueDict(entry, fields):
        field2value = {}
        for field in fields:
            value = entry.get(field)
            if value is not None:
                field2value[field] = value
        return field2value

    @staticmethod
    def _mergeFieldValueDicts(dict1, dict2):
        mergedDict = dict(dict1)
        mergeConflicts = {}
        for k, v in dict2.items():
            if k in mergedDict:  # Key exists in both dicts
                other_v = mergedDict[k]
                if v != other_v:  # Value conflict detected, entry
                    print('WARNING: Value conflict detected for field {}: "{}" vs "{}"'.format(k, v, other_v))
                    mergedDict[k] = None
                    mergeConflicts[k] = [other_v, v]
            else:  # New key-value pair, add to dict
                mergedDict[k] = v
        return mergedDict, mergeConflicts

    @classmethod
    def removeNoneFromDict(cls, noneDict):
        cleanedDict = {}
        for k, v in noneDict.items():
            if type(v) == dict:
                v = cls.removeNoneFromDict(v)

            if v is not None:
                cleanedDict[k] = v

        if cleanedDict:
            return cleanedDict
        else:
            return None


def fixEntries(entries, config, show):
    # Check for Duplicates #
    # Duplicate keys
    if config.duplicateKeys:
        print(NOT_IMPLEMENTED_PATTERN.format("duplicate keys"))

    # Duplicate titles
    if config.duplicateTitles:
        # duplicateTitles = nanny.findDuplicateTitles(entries)
        print(NOT_IMPLEMENTED_PATTERN.format("duplicate titles"))

    # Missing fields #
    # Missing required fields
    if config.anyMissingFields:
        inferrer = FieldInferrer(entries)
        if config.missingRequiredFields:
            print(NOT_IMPLEMENTED_PATTERN.format("missing required fields"))
        # Missing optional fields
        if config.missingOptionalFields:
            print(NOT_IMPLEMENTED_PATTERN.format("missing optional fields"))

            # for key, entry in entries.items():
            #     availability2fields = nanny.getFieldAvailability(entry)
            #     missingOptionalFields = availability2fields[nanny.FIELD_IS_OPTIONAL_MISSING]
            #     if show.missingOptionalFields and missingOptionalFields:
            #         print(key, missingOptionalFields)
            # if show.missingOptionalFields:
            #     print()

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    if config.unsecuredTitleChars:
        key2unsecuredChars = nanny.findUnsecuredUppercase(entries)
        if key2unsecuredChars:
            if show.unsecuredTitleChars:
                print(HEADLINE_PATTERN.format("Securing uppercase characters in titles with curly braces"))
            for key, unsecuredChars in key2unsecuredChars.items():
                entry = entries[key]
                original_title = entry[nanny.FIELD_TITLE]
                fixed_title = fixUnsecuredUppercase(original_title, unsecuredChars)
                entry[nanny.FIELD_TITLE] = fixed_title
                if show.unsecuredTitleChars:
                    print("Fixed {} unsecured uppercase characters in entry {}".format(len(unsecuredChars), key))
                    print("  Before: {}".format(original_title))
                    print("  After:  {}".format(fixed_title))
            if show.unsecuredTitleChars:
                print()

    # Unnecessary curly braces
    if config.unnecessaryBraces:
        print(NOT_IMPLEMENTED_PATTERN.format("unnecessary curly braces"))

    # Bad page number hyphens
    if config.badPageNumbers:
        badPageNumberEntries = nanny.findBadPageNumbers(entries)
        if badPageNumberEntries:
            if show.badPageNumbers:
                print(HEADLINE_PATTERN.format("Fixing page numbers"))
            for entry in badPageNumberEntries:
                original_pages = entry[nanny.FIELD_PAGES]
                fixed_pages = fixBadPageNumbers(original_pages)
                entry[nanny.FIELD_PAGES] = fixed_pages
                if show.badPageNumbers:
                    print("Fixed page numbers for entry {}".format(entry.key))
                    print("  Before: {}".format(original_pages))
                    print("  After:  {}".format(fixed_pages))
            if show.badPageNumbers:
                print()

    # Inconsistent Formatting #
    # Inconsistent names for conferences
    if config.inconsistentConferences:
        print(NOT_IMPLEMENTED_PATTERN.format("inconsistent names for conferences"))

    # Inconsistent name initials formatting
    if config.inconsistentNames:
        print(NOT_IMPLEMENTED_PATTERN.format("inconsistent name initials formatting"))

    # Inconsistent location names
    if config.inconsistentLocations:
        print(NOT_IMPLEMENTED_PATTERN.format("inconsistent names for conferences"))


def fixUnsecuredUppercase(text, unsecuredChars):
    unsecuredChars = set(unsecuredChars)
    fixed_chars = []
    lastCharWasClosingCurlyBrace = False
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


def fixBadPageNumbers(pages):
    pages = pages.replace(' ', '')
    while '---' in pages:
        pages = pages.replace('---', '--')
    if RE_NOTPAGES_CHAR.search(pages):
        pages = RE_NOTPAGES_CHAR.sub('', pages)
    return pages


def main():
    parser = argparse.ArgumentParser(description='Check the consistency of BibTeX entries.')
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('-a', '--aux')
    parser.add_argument('-c', '--config')

    args = parser.parse_args()

    # Load BibTex file
    entries, preamble = nanny.loadBibTex(args.input, loadPreamble=True)

    # Load auxiliary file
    all_entries = entries
    if args.aux:
        keyWhitelist = nanny.loadCitedKeys(args.aux)
        entries = nanny.filterEntries(entries, keyWhitelist)

    # Load config file
    config = FixerConfig(args.config)
    silentconfig = FixerSilentModeConfig(args.config)

    # Processing
    fixEntries(entries, config, silentconfig)

    # Save fixed BibTex file
    nanny.saveBibTex(args.output, all_entries, preamble,
                     month_to_macro=True, wrap_width=None, bibdesk_compatible=True)


if __name__ == '__main__':
    main()
