"""
Collection of functions used by various tools of the BibTexNanny toolkit.
"""

import sys
import os
import re
import configparser
from collections import OrderedDict, namedtuple, Counter
from abc import ABC, abstractmethod

from aux.biblib import bib

__author__ = 'Marc Schulder'


FIELD_TITLE = 'title'
FIELD_PAGES = 'pages'

FIELD_IS_REQUIRED_AVAILABLE = 'required available'
FIELD_IS_REQUIRED_MISSING = 'required missing'
FIELD_IS_OPTIONAL_AVAILABLE = 'optional available'
FIELD_IS_OPTIONAL_MISSING = 'optional missing'
FIELD_IS_ADDITIONAL = 'additional'

TYPE2REQUIRED_FIELDS = {'article': {'author', 'title', 'journal', 'year', 'volume'},
                        'book': {'author', 'editor', 'title', 'publisher', 'year'},
                        'booklet': {'title'},
                        'conference': {'author', 'title', 'booktitle', 'year'},
                        'inbook': {'author', 'editor', 'title', 'chapter', 'pages', 'publisher', 'year'},
                        'incollection': {'author', 'title', 'booktitle', 'publisher', 'year'},
                        'inproceedings': {'author', 'title', 'booktitle', 'year'},
                        'manual': {'title'},
                        'mastersthesis': {'author', 'title', 'school', 'year'},
                        'misc': {},
                        'phdthesis': {'author', 'title', 'school', 'year'},
                        'proceedings': {'title', 'year'},
                        'techreport': {'author', 'title', 'institution', 'year'},
                        'unpublished': {'author', 'title', 'note'},
                        }
TYPE2REQUIRED_ALTERNATIVES = {'book': {'author': 'editor', 'editor': 'author'},
                              'inbook': {'author': 'editor', 'editor': 'author',
                                         'chapter': 'pages', 'pages': 'chapter'},
                              }

TYPE2OPTIONAL_FIELDS = {'article': {'number', 'pages', 'month', 'note', 'key'},
                        'book': {'volume', 'number', 'series', 'address', 'edition', 'month', 'note', 'key', 'url'},
                        'booklet': {'author', 'howpublished', 'address', 'month', 'year', 'note', 'key'},
                        'conference': {'editor', 'volume', 'number', 'series', 'pages', 'address', 'month',
                                       'organization', 'publisher', 'note', 'key'},
                        'inbook': {'volume', 'number', 'series', 'type', 'address', 'edition', 'month', 'note', 'key'},
                        'incollection': {'editor', 'volume', 'number', 'series', 'type', 'chapter', 'pages', 'address',
                                         'edition', 'month', 'note', 'key'},
                        'inproceedings': {'editor', 'volume', 'number', 'series', 'pages', 'address', 'month',
                                          'organization', 'publisher', 'note', 'key'},
                        'manual': {'author', 'organization', 'address', 'edition', 'month', 'year', 'note', 'key'},
                        'mastersthesis': {'type', 'address', 'month', 'note', 'key'},
                        'misc': {'author', 'title', 'howpublished', 'month', 'year', 'note', 'key'},
                        'phdthesis': {'type', 'address', 'month', 'note', 'key'},
                        'proceedings': {'editor', 'volume', 'number', 'series', 'address', 'month', 'publisher',
                                        'organization', 'note', 'key'},
                        'techreport': {'type', 'number', 'address', 'month', 'note', 'key'},
                        'unpublished': {'month', 'year', 'key'},
                        }

TYPE2OPTIONAL_ALTERNATIVES = {'book': {'volume': 'number', 'number': 'volume'},
                              'inbook': {'volume': 'number', 'number': 'volume'},
                              'incollection': {'volume': 'number', 'number': 'volume'},
                              'inproceedings': {'volume': 'number', 'number': 'volume'},
                              'proceedings': {'volume': 'number', 'number': 'volume'},
                              }


class NannyConfig(ABC):
    SECTION = 'DEFAULT'
    FALLBACK = None

    def __init__(self, filename=None, fallback=FALLBACK):
        self.duplicateKeys = fallback
        self.duplicateTitles = fallback
        self.missingRequiredFields = fallback
        self.missingOptionalFields = fallback
        self.unsecuredTitleChars = fallback
        self.unnecessaryBraces = fallback
        self.badPageNumbers = fallback
        self.inconsistentConferences = fallback
        self.incompleteNames = fallback
        self.inconsistentNames = fallback
        self.inconsistentLocations = fallback
        self.inconsistentInferrableInfo = fallback

        self._setAnyMissingFieldsValue()

        if filename is not None:
            self.load(filename)

    def load(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        self.setUpConfig(config)

    def setUpConfig(self, config):
        section = config[self.SECTION]
        self.duplicateKeys = self._getConfigValue(section, 'Duplicate Keys')
        self.duplicateTitles = self._getConfigValue(section, 'Duplicate Titles')
        self.missingRequiredFields = self._getConfigValue(section, 'Missing Required Fields')
        self.missingOptionalFields = self._getConfigValue(section, 'Missing Optional Fields')
        self.unsecuredTitleChars = self._getConfigValue(section, 'Unsecured Title Characters')
        self.unnecessaryBraces = self._getConfigValue(section, 'Unnecessary Braces')
        self.badPageNumbers = self._getConfigValue(section, 'Bad Page Numbers')
        self.inconsistentConferences = self._getConfigValue(section, 'Inconsistent Conferences')
        self.incompleteNames = self._getConfigValue(section, 'Incomplete Names')
        self.inconsistentNames = self._getConfigValue(section, 'Inconsistent Names')
        self.inconsistentLocations = self._getConfigValue(section, 'Inconsistent Locations')
        self.inconsistentInferrableInfo = self._getConfigValue(section, 'Inconsistent Inferrable Information')

        self._setAnyMissingFieldsValue()

    def _setAnyMissingFieldsValue(self):
        if self.missingRequiredFields is None:
            if self.missingOptionalFields is None:
                return None
            else:
                return self.missingOptionalFields
        else:
            if self.missingOptionalFields is None:
                return self.missingRequiredFields
            else:
                self.anyMissingFields = max(self.missingRequiredFields, self.missingOptionalFields)

    @abstractmethod
    def _getConfigValue(self, section, key, fallback=FALLBACK):
        pass


class FieldInferrer:
    ACTION_ADD = 'ADD'
    
    EventTuple = namedtuple('EventTuple', ('action', 'key', 'field', 'value', 'isRequiredField'))
    
    TYPE2INPUT2INFERRABLE = {
        'incollection':
            {('booktitle', 'year'): ('address', 'month', 'editor', 'publisher')},
        'inproceedings':
            {('booktitle', 'year'): ('address', 'month', 'editor', 'organization', 'publisher')},
    }

    def __init__(self, entries):
        self.log = []
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
                if v != other_v:  # Value conflict detected
                    # print('WARNING: Value conflict detected for field {}: "{}" vs "{}"'.format(k, v, other_v))
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

    def addInformation(self, entry, addRequiredFields, addOptionalFields, verbose=False):
        # Maps a tuple of fields A to a tuple of fields B.
        # If all fields A are known, all fields B can potentially be inferred from another entry
        # with the same values for A.
        input2inferrable = self.TYPE2INPUT2INFERRABLE.get(entry.typ)
        # Mapping specific pieces of information to the information that can be inferred from them.
        # The keys are a tuple of (field, value) tuples and values are field->value dicts
        input2information = self.type2input2information.get(entry.typ)
        # Choose which fields may be edited, based on the user's choice for adding required and optional fields.
        # Is a mapping from the field name to a boolean indicating whether it is a required field
        editableFields2isRequiredField = {}
        if addOptionalFields:
            for optionalField in TYPE2OPTIONAL_FIELDS.get(entry.typ, set()):
                editableFields2isRequiredField[optionalField] = False
        if addRequiredFields:
            for requiredField in TYPE2REQUIRED_FIELDS.get(entry.typ, set()):
                editableFields2isRequiredField[requiredField] = True
        
        # Add inferrable information
        if input2inferrable is not None:
            for inputFields, inferrableFields in input2inferrable.items():
                # Collect this entry's values for its inferrable fields.
                inputValues = self._getAllFieldValues(entry, inputFields)
                if inputValues is not None:
                    infoDict = input2information.get(inputValues)
                    if infoDict is not None:
                        for field, value in infoDict.items():
                            if field in entry:
                                # If the entry already has a value for this field, we need no inference.
                                pass
                            else:
                                if field in editableFields2isRequiredField:
                                    isRequiredField = editableFields2isRequiredField[field]
                                    if verbose:
                                        if isRequiredField:
                                            print('Adding required field "{}" to key "{}": {}'.format(field, entry.key,
                                                                                                      value))
                                        else:
                                            print('Adding optional field "{}" to key "{}": {}'.format(field, entry.key,
                                                                                                      value))
                                    self.log.append(self.EventTuple(action=self.ACTION_ADD, key=entry.key, field=field,
                                                                    value=value, isRequiredField=isRequiredField))
                                    entry[field] = value
    
    def getFieldChangeCount(self):
        action2field2count = {}
        for event in self.log:
            field2count = action2field2count.setdefault(event.action, Counter())
            field2count[event.field] += 1
        return action2field2count


class LocationKnowledge:
    def __init__(self, countryFile, statesFile):
        self.countries2alts = {}
        self.country2short2state = {}
        self.country2state2short = {}

        self.loadCountries(countryFile)
        self.loadStates(statesFile)

    def loadCountries(self, filename):
        pass

    def loadStates(self, filename):
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option
        config.read(filename)
        for sectionName in config.sections():
            short2state = self.country2short2state.setdefault(sectionName, {})
            state2short = self.country2state2short.setdefault(sectionName, {})
            for state, short in config.items(sectionName):
                short2state[short] = state
                state2short[state] = short

    def shortenState(self, country, state):
        return self.country2state2short.get(country, {}).get(state, state)

    def expandState(self, country, state):
        return self.country2short2state.get(country, {}).get(state, state)


class Location:
    def __init__(self, string, locationKnowledge):
        self.knowledge = locationKnowledge
        self.original_string = string
        self.city = None
        self.state = None
        self.country = None
        self._parse(string)

    def _parse(self, string):
        elems = string.split(',')
        elems = [elem.strip() for elem in elems]

        if len(elems) == 1:
            # print(elems[0])
            self.city = elems[0]
        elif len(elems) == 2:
            self.city = elems[0]
            self.country = elems[1]
        elif len(elems) == 3:
            self.city = elems[0]
            self.state = elems[1]
            self.country = elems[2]
        else:
            raise ValueError("Could not read address: {}".format(string))

    def expandInformation(self):
        self.state = self.knowledge.expandState(self.country, self.state)

    def getString(self):
        elems = [elem for elem in [self.city, self.state, self.country] if elem is not None]
        return ', '.join(elems)


def loadBibTex(filename, loadPreamble=False):
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        raise FileNotFoundError(filename)

    preamble = ''
    if loadPreamble:
        # Read preamble
        preamble_lines = []
        with open(filename) as f:
            for line in f:
                if line.strip().startswith('@') and not line.strip().startswith('@comment{'):
                    break
                else:
                    preamble_lines.append(line)
        preamble = ''.join(preamble_lines)

    # Parse BibTex entries
    parser = bib.Parser(repeatKeySuffix="_REPEATKEY")
    with open(filename) as f:
        parser.parse(f, log_fp=sys.stderr)

    entries = parser.get_entries()

    # # Resolve cross-references
    # entries = biblib.bib.resolve_crossrefs(entries)

    if loadPreamble:
        return entries, preamble
    else:
        return entries


def saveBibTex(filename, key2entry, preamble='', month_to_macro=True, wrap_width=70, bibdesk_compatible=False):
    entryStrings = [entry.to_bib(month_to_macro=month_to_macro, wrap_width=wrap_width,
                                 bibdesk_compatible=bibdesk_compatible) for entry in key2entry.values()]
    text = '\n\n'.join(entryStrings)
    with open(filename, 'w') as w:
        w.write(preamble)
        w.write(text)
        w.write('\n')


def loadCitedKeys(filename, lowercaseKeys=False):
    citationRE = re.compile(r"^\\citation{(.*)}$")
    keys = set()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            citationMatch = citationRE.match(line)
            if citationMatch:
                citationString = citationMatch.group(1)
                citations = citationString.split(',')
                for citation in citations:
                    if lowercaseKeys:
                        citation = citation.lower()
                    keys.add(citation)
    return keys


def filterEntries(key2entry, keyWhitelist):
    keyWhitelist = set(keyWhitelist)
    filteredEntries = OrderedDict()

    for key, entry in key2entry.items():
        key = key.lower()
        if key in keyWhitelist:
            filteredEntries[key] = entry

    return filteredEntries


def getFieldAvailability(entry):
    availability = {FIELD_IS_REQUIRED_AVAILABLE: [],
                    FIELD_IS_REQUIRED_MISSING: [],
                    FIELD_IS_OPTIONAL_AVAILABLE: [],
                    FIELD_IS_OPTIONAL_MISSING: [],
                    FIELD_IS_ADDITIONAL: [],
                    }
    unseenRequiredFields = set(TYPE2REQUIRED_FIELDS.get(entry.typ, set()))
    requiredFields = TYPE2REQUIRED_FIELDS.get(entry.typ, set())
    unseenOptionalFields = set(TYPE2OPTIONAL_FIELDS.get(entry.typ, set()))
    optionalFields = TYPE2OPTIONAL_FIELDS.get(entry.typ, set())
    requiredAlts = TYPE2REQUIRED_ALTERNATIVES.get(entry.typ, {})
    optionalAlts = TYPE2OPTIONAL_ALTERNATIVES.get(entry.typ, {})

    for field in entry:
        if field in requiredFields:
            availability[FIELD_IS_REQUIRED_AVAILABLE].append(field)
            unseenRequiredFields.discard(field)
            if field in requiredAlts:
                unseenRequiredFields.discard(requiredAlts[field])
        elif field in optionalFields:
            availability[FIELD_IS_OPTIONAL_AVAILABLE].append(field)
            unseenOptionalFields.discard(field)
            if field in optionalAlts:
                unseenOptionalFields.discard(optionalAlts[field])
        else:
            availability[FIELD_IS_ADDITIONAL].append(field)
    availability[FIELD_IS_REQUIRED_MISSING].extend(unseenRequiredFields)
    availability[FIELD_IS_OPTIONAL_MISSING].extend(unseenOptionalFields)

    return availability


def getFieldAvailabilities(entries):
    key2availability = OrderedDict()
    for key, entry in entries.items():
        key2availability[key] = getFieldAvailability(entry)
    return key2availability


def findDuplicateKeys(entries):
    # Can not be checked for right now because biblib throws errors when encountering repeated keys

    raise UserWarning("Finding duplicate keys is not yet implemented.")

    # duplicates = set()
    # for entry in entries:
    #     print(entry)
    #     break
    # return duplicates


def findDuplicateTitles(entries, ignoreCurlyBraces=True, ignoreCaps=True):
    title2seenEntries = {}
    for key, entry in entries.items():
        title = entry["title"]
        if ignoreCurlyBraces:
            title = title.replace('{', '')
            title = title.replace('}', '')
        if ignoreCaps:
            title = title.lower()

        title2seenEntries.setdefault(title, []).append(entry)

    title2duplicateEntries = {}
    for title, entries in title2seenEntries.items():
        if len(entries) >= 2:
            title2duplicateEntries[title] = entries

    return title2duplicateEntries


def findUnsecuredUppercase(entries):
    """
    Find entries that contain uppercase characters that are not secured by curly braces.
    The only uppercase character that needs no braces is the first letter of the title, as it is automatically
    converted to uppercase anyway.

    Background: In most bibliography styles titles are by defauly displayed with only the first character being
    uppercase and all others are forced to be lowercase. If you want to display any other uppercase characters, you
    have to secure them by wrapping them in curly braces.
    :param entries:
    :return:
    """
    key2unsecuredChars = OrderedDict()
    for key, entry in entries.items():
        if "title" not in entry:
            continue

        title = entry["title"]
        isSecured = False

        # Skip first character (unless it is a curly brace) as it is auto-converted to uppercase anyway
        i_start = 0
        if title[0] != '{':
            title = title[1:]
            i_start = 1

        for i, c in enumerate(title, start=i_start):
            if c == '{':
                isSecured = True
            elif c == '}':
                isSecured = False
            elif not isSecured and c.isupper():
                key2unsecuredChars.setdefault(key, []).append(i)
    return key2unsecuredChars


def findBadPageNumbers(entries, tolerateSingleHyphens=True):
    if tolerateSingleHyphens:
        pageRE = re.compile(r'^{0}(,{0})*$'.format(r'\d+((\-\-\d+)|(\-\d+)|(\+))?'))
    else:
        pageRE = re.compile(r'^{0}(,{0})*$'.format(r'\d+((\-\-\d+)|(\+))?'))

    badEntries = []
    for key, entry in entries.items():
        if "pages" not in entry:
            continue

        pages = entry["pages"]
        if not pageRE.match(pages):
            badEntries.append(entry)
    return badEntries
