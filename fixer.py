"""
Fixes BibTeX entries.
"""

import re
import argparse
import unicodedata
from collections import OrderedDict, Counter

from aux import nanny, biblib
from aux.unicode2bibtex import unicode2bibtex, unicodeCombiningCharacter2bibtex

__author__ = 'Marc Schulder'

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

    def _getConfigList(self, section, key, separator=','):
        value = section.get(key, fallback=None)
        if value is None:
            return []
        else:
            items = [item.strip() for item in value.split(separator)]
            return items


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

    def _getConfigList(self, section, key, separator=','):
        value = section.get(key, fallback=None)
        if value is None:
            return []
        else:
            items = [item.strip() for item in value.split(separator)]
            return items


class ChangeLogger:
    HEADLINE_PATTERN = "===== {} ====="
    SUMMARY_HEADLINE_PATTERN = "===== Summary: {} ====="

    def __init__(self, headline=None, verbosity=None):
        self.headline = headline
        self.verbosity = verbosity
        self.currentKey = None
        self.key2changes = OrderedDict()

    def __str__(self):
        self.getLog()

    def getLog(self):
        lines = []

        if self.headline is not None:
            lines.append(self.HEADLINE_PATTERN.format(self.headline))

        for key, changes in self.key2changes.items():
            lines.append('Changes to entry {}'.format(key))
            for info, original, changed in changes:
                if original is None and changed is None:
                    lines.append('  {}')
                elif changed is None:
                    lines.append('  {}: {}'.format(info, original))
                elif original is None:
                    lines.append('  {}: {}'.format(info, changed))
                else:
                    indent = ' ' * len(info)
                    lines.append('  {}: {}'.format(info, original))
                    lines.append('{} => {}'.format(indent, changed))

        return '\n'.join(lines)

    def getSummary(self):
        lines = []

        if self.headline is not None:
            lines.append(self.SUMMARY_HEADLINE_PATTERN.format(self.headline))

        lines.append('{} entries affected'.format(len(self.key2changes)))

        eventCounter = Counter()
        for key, changes in self.key2changes.items():
            for info, original, changed in changes:
                eventCounter[info] += 1

        if len(eventCounter) > 0:
            max_n = eventCounter.most_common(1)[0][1]
            max_digits = len(str(max_n))

            lines.append('Actions:')
            for event, count in eventCounter.most_common():
                digits = len(str(count))
                indent = ' ' * (max_digits - digits)
                lines.append('  {}{} x {}'.format(indent, count, event))

        return '\n'.join(lines)

    def containsChanges(self):
        return len(self.key2changes) > 0

    def setCurrentKey(self, key):
        self.currentKey = key

    def logNameObjectDiff(self, info, original, changed):
        if original != changed:
            self.addChange4CurrentEntry(info, getNamesString(original), getNamesString(changed))

    def addChange(self, key, info, original, changed):
        change = (info, original, changed)
        changes = self.key2changes.setdefault(key, [])
        changes.append(change)

    def addChange4CurrentEntry(self, info, original, changed):
        change = (info, original, changed)
        changes = self.key2changes.setdefault(self.currentKey, [])
        changes.append(change)

    def printLog(self):
        if self.containsChanges:
            if self.verbosity >= FixerSilentModeConfig.SHOW:
                print(self.getLog())
                print()
            elif self.verbosity >= FixerSilentModeConfig.SUMMARY:
                print(self.getSummary())
                print()


def fixEntries(entries, config, show):
    # Fix encoding #
    # LaTeX to BibTex formatting
    if config.latex2unicode or config.unicode2bibtex:
        if config.latex2unicode and config.unicode2bibtex:
            logger = ChangeLogger("Converting LaTeX/Unicode to BibTeX",
                                  verbosity=max(show.latex2unicode, show.unicode2bibtex))
        elif config.latex2unicode:
            logger = ChangeLogger("Converting LaTeX to Unicode",
                                  verbosity=show.latex2unicode)
        else:
            logger = ChangeLogger("Converting Unicode to BibTeX",
                                  verbosity=show.unicode2bibtex)

        for entry_key, entry in entries.items():
            logger.setCurrentKey(entry_key)
            for field, value in entry.items():
                convertedValue = value
                if '&' in value:
                    print('@@@', convertedValue)
                if config.latex2unicode:
                    convertedValue = convertLaTeX2Unicode(convertedValue)
                    if '&' in value:
                        print('###', convertedValue)
                if config.unicode2bibtex:
                    convertedValue = convertUnicode2BibTeX(convertedValue)
                    if '&' in value:
                        print('$$$', convertedValue)
                        print()

                if convertedValue != value:
                    entry[field] = convertedValue
                    logger.addChange4CurrentEntry('Converted LaTeX to Unicode', value, convertedValue)
        logger.printLog()

    # Check for Duplicates #
    # Duplicate keys
    if config.duplicateKeys:
        print(NOT_IMPLEMENTED_PATTERN.format("duplicate keys"))

    # Duplicate titles
    if config.duplicateTitles:
        # duplicateTitles = nanny.findDuplicateTitles(entries)
        print(NOT_IMPLEMENTED_PATTERN.format("duplicate titles"))

    # Bad Formatting #
    # Replace non-ASCII characters in key
    if config.asciiKeys:
        keyChanges = []
        logger = ChangeLogger("Converting entry keys to be ASCII-compliant",
                              verbosity=show.asciiKeys)
        for entry_key, entry in entries.items():
            logger.setCurrentKey(entry_key)
            fixed_key = entry.key.replace('ß', 'ss')
            fixed_key = unicodedata.normalize('NFKD', fixed_key).encode('ascii', 'ignore').decode('ascii')
            if fixed_key != entry.key:

                keyChanges.append((entry_key, fixed_key, entry))
                logger.addChange4CurrentEntry('Fixed a non-ASCII key', entry.key, fixed_key)
        for entry_key, fixed_key, entry in keyChanges:
            entry.key = fixed_key
            del entries[entry_key]
            entries[fixed_key.lower()] = entry
        logger.printLog()

    # Unsecured uppercase characters in titles
    if config.unsecuredTitleChars:
        logger = ChangeLogger("Securing uppercase characters in titles with curly braces",
                              verbosity=show.unsecuredTitleChars)
        key2unsecuredChars = nanny.findUnsecuredUppercase(entries, field=nanny.FIELD_TITLE)
        if key2unsecuredChars:
            for key, unsecuredChars in key2unsecuredChars.items():
                logger.setCurrentKey(key)
                entry = entries[key]
                original_title = entry[nanny.FIELD_TITLE]
                fixed_title = fixUnsecuredUppercase(original_title, unsecuredChars)
                entry[nanny.FIELD_TITLE] = fixed_title
                logger.addChange4CurrentEntry('Fixed {} unsecured uppercase characters'.format(len(unsecuredChars)),
                                              original_title, fixed_title)
        logger.printLog()
    # Unnecessary curly braces
    if config.unnecessaryBraces:
        print(NOT_IMPLEMENTED_PATTERN.format("unnecessary curly braces"))

    # Bad page number hyphens
    if config.badPageNumbers:
        logger = ChangeLogger("Fixing page numbers",
                              verbosity=show.badPageNumbers)
        badPageNumberEntries = nanny.findBadPageNumbers(entries)
        if badPageNumberEntries:
            for entry in badPageNumberEntries:
                logger.setCurrentKey(entry.key)
                original_pages = entry[nanny.FIELD_PAGES]
                fixed_pages = fixBadPageNumbers(original_pages)
                
                if fixed_pages == original_pages:
                    # Fixing page numbers failed
                    logger.addChange4CurrentEntry('Failed to fix bad page numbers', original_pages, None)
                else:
                    # Fixing page numbers forked
                    entry[nanny.FIELD_PAGES] = fixed_pages
                    logger.addChange4CurrentEntry('Fixed page numbers', original_pages, fixed_pages)

    # Inconsistent Formatting #
    # Inconsistent names for conferences
    if config.inconsistentConferences:
        print(NOT_IMPLEMENTED_PATTERN.format("inconsistent names for conferences"))

    # Ambiguous name formatting
    if config.ambiguousNames:
        logger = ChangeLogger("Fixing names",
                              verbosity=show.ambiguousNames)
        badNameEntries = fixNames(entries, logger, not config.latex2unicode, not config.unicode2bibtex)
        logger.printLog()

    # All-caps name formatting
    # if config.ambiguousNames:
    #     print(NOT_IMPLEMENTED_PATTERN.format("all-caps name formatting"))

    # Inconsistent location names
    if config.inconsistentLocations:
        logger = ChangeLogger("Fixing incomplete location names",
                              verbosity=show.inconsistentLocations)
        locationKnowledge = nanny.LocationKnowledge(countryFile='info/countries.config',
                                                    statesFile='info/states.config')
        # TODO: Also use information from other entries to expand this one
        for key, entry in nanny.getEntriesWithField(entries, nanny.FIELD_ADDRESS):
            logger.setCurrentKey(key)
            address = entry[nanny.FIELD_ADDRESS]
            location = nanny.Location(address, locationKnowledge)
            location.expandInformation()
            fixedAddress = location.getString()
            if fixedAddress != address:
                entry[nanny.FIELD_ADDRESS] = fixedAddress
                logger.addChange4CurrentEntry('Fixed address info', address, fixedAddress)
        logger.printLog()

    # Missing fields #
    # Missing required fields
    if config.anyMissingFields:
        logger = ChangeLogger("Adding missing information",
                              verbosity=show.anyMissingFields)
        # Infer information
        inferrer = nanny.FieldInferrer(entries)
        for key, entry in entries.items():
            inferrer.addInformation(entry,
                                    addRequiredFields=config.missingRequiredFields,
                                    addOptionalFields=config.missingOptionalFields,
                                    logger=logger,
                                    verbose=show.anyMissingFields >= FixerSilentModeConfig.SHOW)
        
        logger.printLog()

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


def fixNames(entries, logger, fixLaTeX=True, fixUnicode=True):
    key2badEntries = OrderedDict()
    for entry_key, entry in entries.items():
        logger.setCurrentKey(entry_key)

        isBadEntry = False
        for field in nanny.PERSON_NAME_FIELDS:
            if field in entry:
                names = entry.authors(field)

                # Check name formatting
                names_string = getNamesString(names)
                if names_string != entry.get(field):
                    logger.addChange4CurrentEntry('BibTeX name format has changed', entry.get(field), names_string)

                fixed_names = []
                for name in names:
                    if name.is_others():
                        fixed_names.append(name)
                    else:
                        fixed_name = fixControlSequences(name, logger, fixLaTeX, fixUnicode)
                        fixed_name = fixNameInitials(fixed_name, logger)
                        fixed_name = fixAllCapsNames(fixed_name, logger)
                        fixed_names.append(fixed_name)

                # Convert Name objects to multi-author string
                names_string = getNamesString(fixed_names)
                if names_string != entry.get(field):
                    isBadEntry = True
                    # print(names_string)
                    entry[field] = names_string
                    try:
                        names_string.encode('ascii')
                    except UnicodeEncodeError:
                        print("Bad encoding: {}".format(names_string))
        if isBadEntry:
            key2badEntries[entry_key] = entry

        # nanny.findAllCapsName(entries, 'author')
    return key2badEntries


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def getNamesString(names, template='{von} {last}, {jr}, {first}'):
    if isinstance(names, biblib.algo.Name):
        return names.pretty(template)
    else:
        return ' and '.join([name.pretty(template) for name in names])


def fixControlSequences(name, logger, fixLaTeX, fixUnicode):
    if fixLaTeX or fixUnicode:
        name_dict = name._asdict()
        for name_key, name_elem in name_dict.items():
            if len(name_elem) > 0:
                if fixLaTeX:
                    name_elem = convertLaTeX2Unicode(name_elem)
                if fixUnicode:
                    name_elem = convertUnicode2BibTeX(name_elem)
                name_dict[name_key] = name_elem
        fixed_name = name._replace(**name_dict)
        logger.logNameObjectDiff('Fixed control sequences', name, fixed_name)
        return fixed_name
    else:
        return name


def fixNameInitials(name, logger):
    initialsRE = re.compile(r'(\w\.)+?')
    name_dict = name._asdict()
    rerun_fix = False
    for name_key, name_elem in name_dict.items():
        fixed_subelems = []
        name_subelems = name_elem.split()
        for i, name_subelem in enumerate(name_subelems):
            if len(name_subelem) == 1:
                fixed_subelem = '{}.'.format(name_subelem)
            else:
                fixed_subelem = initialsRE.sub(r'\1 ', name_subelem).strip()
                if fixed_subelem != name_subelem:
                    rerun_fix = True
            fixed_subelems.append(fixed_subelem)
        name_dict[name_key] = ' '.join(fixed_subelems)
    fixed_name = name._replace(**name_dict)

    if rerun_fix:
        fixed_name = fixNameInitials(fixed_name, logger)
    else:
        logger.logNameObjectDiff('Fixed name initials', name, fixed_name)
    return fixed_name


def fixAllCapsNames(name, logger):
    name_dict = name._asdict()
    for name_key, name_elem in name_dict.items():
        if len(name_elem) > 0:
            name_subelems = name_elem.split(' ')
            fixed_subelems = []
            for i, name_subelem in enumerate(name_subelems):
                if name_subelem.isupper():
                    if len(name_subelem) <= 3:
                        fixed_subelem = name_subelem
                    else:
                        fixed_subelem = name_subelem.capitalize()
                else:
                    fixed_subelem = name_subelem
                fixed_subelems.append(fixed_subelem)
            name_dict[name_key] = ' '.join(fixed_subelems)
    fixed_name = name._replace(**name_dict)
    logger.logNameObjectDiff('Fixed all-caps name (or part of name)', name, fixed_name)
    return fixed_name


def convertLaTeX2Unicode(string):
    string = nanny.fixTexInNameElement(string)
    # try:
    #     string = biblib.algo.tex_to_unicode(string)
    # except biblib.messages.InputError as e:
    #     pass
    string = biblib.algo.tex_to_unicode(string)
    # todo: More Latex conversions
    return string


def convertUnicode2BibTeX(string):
    unicode_chars = []
    lastChar = None
    isMathMode = False
    for c, char in enumerate(string):
        if isMathMode:
            unicode_chars.append(char)
            if char == '$' and lastChar != '\\':
                isMathMode = False
        else:
            if char == '$' and lastChar != '\\':  # Start of mathmode
                print(c, string)
                unicode_chars.append(char)
                isMathMode = True
            elif char == '$' and lastChar == '\\':  # Special handling for escaped dollar sign
                del unicode_chars[-1]
                unicode_chars.append(unicode2bibtex[char])
            elif char in unicode2bibtex:  # Unicode character requires conversion
                unicode_chars.append(unicode2bibtex[char])
            elif char in unicodeCombiningCharacter2bibtex:  # Is combining character, read next char
                pass
                if len(unicode_chars) > 0 and unicode_chars[-1] == ' ':  # Delete unicode space
                    del unicode_chars[-1]
            elif lastChar in unicodeCombiningCharacter2bibtex:  # Merge char with previous combining char
                combinedCharacter = unicodeCombiningCharacter2bibtex[lastChar].format(char)
                unicode_chars.append(combinedCharacter)
            else:  # Not a special char, read in normally
                unicode_chars.append(char)
        lastChar = char

    # Clean up if final char was a combining character
    if not isMathMode and lastChar in unicodeCombiningCharacter2bibtex:
        combinedCharacter = unicodeCombiningCharacter2bibtex[lastChar].format('{}')
        unicode_chars.append(combinedCharacter)

    return ''.join(unicode_chars)


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
