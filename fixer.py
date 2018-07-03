"""
Fixes BibTeX entries.
"""

import re
import argparse

from aux import nanny

__author__ = 'Marc Schulder'

HEADLINE_PATTERN = "===== {} ====="
NOT_IMPLEMENTED_PATTERN = "Auto-fix for {} not yet implemented"

RE_PAGES_RANGE = re.compile(r'(?P<num1>[0-9]+)(\s*(-+|–|—)\s*)(?P<num2>[0-9]+)')

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

    SHOW = 2
    SUMMARY = 1
    HIDE = 0

    FALLBACK_VALUE = SHOW

    CONFIGVALUE2INTERNAL = {'show': SHOW,
                            'true': SHOW,
                            str(SHOW): SHOW,
                            True: SHOW,
                            'summary': SUMMARY,
                            str(SUMMARY): SUMMARY,
                            'hide': HIDE,
                            'false': HIDE,
                            str(HIDE): HIDE,
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


def fixEntries(entries, config, show):
    # Check for Duplicates #
    # Duplicate keys
    if config.duplicateKeys:
        print(NOT_IMPLEMENTED_PATTERN.format("duplicate keys"))

    # Duplicate titles
    if config.duplicateTitles:
        # duplicateTitles = nanny.findDuplicateTitles(entries)
        print(NOT_IMPLEMENTED_PATTERN.format("duplicate titles"))

    # Bad Formatting #
    # Unsecured uppercase characters in titles
    if config.unsecuredTitleChars:
        key2unsecuredChars = nanny.findUnsecuredUppercase(entries)
        if key2unsecuredChars:
            if show.unsecuredTitleChars >= FixerSilentModeConfig.SUMMARY:
                print(HEADLINE_PATTERN.format("Securing uppercase characters in titles with curly braces"))
            for key, unsecuredChars in key2unsecuredChars.items():
                entry = entries[key]
                original_title = entry[nanny.FIELD_TITLE]
                fixed_title = fixUnsecuredUppercase(original_title, unsecuredChars)
                entry[nanny.FIELD_TITLE] = fixed_title
                if show.unsecuredTitleChars >= FixerSilentModeConfig.SHOW:
                    print("Fixed {} unsecured uppercase characters in entry {}".format(len(unsecuredChars), key))
                    print("  Before: {}".format(original_title))
                    print("  After:  {}".format(fixed_title))
            if show.unsecuredTitleChars >= FixerSilentModeConfig.SUMMARY:
                print()

    # Unnecessary curly braces
    if config.unnecessaryBraces:
        print(NOT_IMPLEMENTED_PATTERN.format("unnecessary curly braces"))

    # Bad page number hyphens
    if config.badPageNumbers:
        badPageNumberEntries = nanny.findBadPageNumbers(entries)
        if badPageNumberEntries:
            if show.badPageNumbers >= FixerSilentModeConfig.SUMMARY:
                print(HEADLINE_PATTERN.format("Fixing page numbers"))
            for entry in badPageNumberEntries:
                original_pages = entry[nanny.FIELD_PAGES]
                fixed_pages = fixBadPageNumbers(original_pages)
                
                if fixed_pages == original_pages:
                    # Fixing page numbers failed
                    if show.badPageNumbers >= FixerSilentModeConfig.SHOW:
                        print("Failed to fix bad page numbers for entry {}: {}".format(entry.key, original_pages))
                else:
                    # Fixing page numbers forked
                    entry[nanny.FIELD_PAGES] = fixed_pages
                    if show.badPageNumbers >= FixerSilentModeConfig.SHOW:
                        print("Fixed page numbers for entry {}".format(entry.key))
                        print("  Before: {}".format(original_pages))
                        print("  After:  {}".format(fixed_pages))
            if show.badPageNumbers >= FixerSilentModeConfig.SUMMARY:
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
        locationKnowledge = nanny.LocationKnowledge(countryFile='info/countries.config', statesFile='info/states.config')
        if show.inconsistentLocations >= FixerSilentModeConfig.SUMMARY:
            print(HEADLINE_PATTERN.format("Fixing incomplete location names"))
            # TODO: Also use information from other entries to expand this one
        for key, entry in entries.items():
            if 'address' in entry:
                address = entry['address']
                location = nanny.Location(address, locationKnowledge)
                location.expandInformation()
                fixedAddress = location.getString()
                if fixedAddress != address:
                    entry['address'] = fixedAddress
                    if show.inconsistentLocations >= FixerSilentModeConfig.SHOW:
                        print("Fixed address info for entry {}".format(entry.key))
                        print("  Before: {}".format(address))
                        print("  After:  {}".format(fixedAddress))
        if show.inconsistentLocations >= FixerSilentModeConfig.SUMMARY:
            print()

    # Missing fields #
    # Missing required fields
    if config.anyMissingFields:
        if show.anyMissingFields >= FixerSilentModeConfig.SUMMARY:
            print(HEADLINE_PATTERN.format("Adding missing information"))
        
        # Infer information
        inferrer = nanny.FieldInferrer(entries)
        for key, entry in entries.items():
            inferrer.addInformation(entry,
                                    addRequiredFields=config.missingRequiredFields,
                                    addOptionalFields=config.missingOptionalFields,
                                    verbose=show.anyMissingFields >= FixerSilentModeConfig.SHOW)
        
        # Summary
        if show.anyMissingFields >= FixerSilentModeConfig.SUMMARY:
            action2field2count = inferrer.getFieldChangeCount()
            field2count = action2field2count.get(inferrer.ACTION_ADD)
            if field2count:
                print("Summary: Added information")
                for field, count in field2count.items():
                    print('  Added {count} "{field}" fields'.format(field=field, count=count))
        
        if show.anyMissingFields >= FixerSilentModeConfig.SUMMARY:
            print()

        # if config.missingRequiredFields:
        #     print(NOT_IMPLEMENTED_PATTERN.format("missing required fields"))
        # # Missing optional fields
        # if config.missingOptionalFields:
        #     print(NOT_IMPLEMENTED_PATTERN.format("missing optional fields"))


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
    pages = RE_PAGES_RANGE.sub(r'\g<num1>--\g<num2>', pages)
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
