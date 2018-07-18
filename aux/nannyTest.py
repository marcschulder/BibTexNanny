import sys
from unittest import TestCase, expectedFailure
from collections import OrderedDict

import fixer
from aux import nanny
from aux.biblib import bib, algo


TYPEFIELD = '@type'
DEFAULT_KEY_START = 'foobar'
DEFAULT_KEY = '{}{}'.format(DEFAULT_KEY_START, 2018)

FIELD_AUTHOR = 'author'
FIELD_TITLE = 'Title'
FIELD_PAGES = 'Pages'


def parse(text):
    parser = bib.Parser()
    parser.parse(text, log_fp=sys.stderr)
    return parser.get_entries()


def getStringEntries(field2valueyDicts, keyStart=DEFAULT_KEY_START):
    entries = [getStringEntry(field2value,
                              key='{}{}'.format(keyStart, i)) for i, field2value in enumerate(field2valueyDicts)]
    return '\n\n'.join(entries)


def getStringEntry(field2value, key=DEFAULT_KEY):
    entryPattern = '@{type}{{{key},\n{fields}}}'
    fieldPattern = '	{field} = {{{value}}},'

    entryType = field2value.get(TYPEFIELD, 'incollection')
    fieldLines = []
    for field, value in field2value.items():
        if field != TYPEFIELD:
            fieldLine = fieldPattern.format(field=field, value=value)
            fieldLines.append(fieldLine)
    entry = entryPattern.format(type=entryType, key=key, fields='\n'.join(fieldLines))
    return entry


class TestFindDuplicateTitles(TestCase):
    def test_findDuplicateTitles_Identical(self):
        title = 'Towards a new test environment'
        entryString = getStringEntries([{FIELD_TITLE: title},
                                        {FIELD_TITLE: title},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Lowercase(self):
        title = 'Towards a New Test Environment'
        entryString = getStringEntries([{FIELD_TITLE: title},
                                        {FIELD_TITLE: title.lower()},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Braces(self):
        title = 'Towards a {N}ew {T}est {E}nvironment'
        unbraced_title = title.replace('{', '').replace('}', '')
        entryString = getStringEntries([{FIELD_TITLE: unbraced_title},
                                        {FIELD_TITLE: title},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {unbraced_title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Braces2(self):
        title = 'Towards a {N}ew {T}est {E}nvironment'
        unbraced_title = title.replace('{', '').replace('}', '')
        entryString = getStringEntries([{FIELD_TITLE: title},
                                        {FIELD_TITLE: unbraced_title},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(2)]
        goldTitle2keys = {unbraced_title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_BracesAndLowercase(self):
        title = 'Towards a {N}ew {T}est {E}nvironment'
        unbraced_title = title.replace('{', '').replace('}', '')
        entryString = getStringEntries([{FIELD_TITLE: unbraced_title},
                                        {FIELD_TITLE: title},
                                        {FIELD_TITLE: unbraced_title.lower()},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(3)]
        goldTitle2keys = {unbraced_title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)

    def test_findDuplicateTitles_Spaces(self):
        title = 'Towards a new test environment'
        entryString = getStringEntries([{FIELD_TITLE: title},
                                        {FIELD_TITLE: 'Towards a new   test environment'},
                                        {FIELD_TITLE: 'Towards a new test environment '},
                                        {FIELD_TITLE: '  Towards a new test environment'},
                                        ])
        goldKeys = ['{}{}'.format(DEFAULT_KEY_START, i) for i in range(4)]
        goldTitle2keys = {title.lower(): goldKeys}
        duplicateTitle2entries = nanny.findDuplicateTitles(parse(entryString))
        duplicateTitle2keys = {title: [e.key for e in entries] for title, entries in duplicateTitle2entries.items()}
        self.assertEqual(duplicateTitle2keys, goldTitle2keys)


class TestFindUnsecuredUppercase(TestCase):
    def test_findUnsecuredUppercase_Basic(self):
        entryString = getStringEntry({FIELD_TITLE: 'Logic and Conversation'})
        key2goldChars = {DEFAULT_KEY: [10]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString), field="title")
        self.assertEqual(key2unsecuredChars, key2goldChars)

    def test_findUnsecuredUppercase_InWord(self):
        entryString = getStringEntry({FIELD_TITLE: 'Aligning {G}ermaNet {S}enses'})
        key2goldChars = {DEFAULT_KEY: [16]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString), field="title")
        self.assertEqual(key2unsecuredChars, key2goldChars)

    def test_findUnsecuredUppercase_AllUpper(self):
        entryString = getStringEntry({FIELD_TITLE: 'WORD ASSOCIATION'})
        key2goldChars = {DEFAULT_KEY: [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString), field="title")
        self.assertEqual(key2unsecuredChars, key2goldChars)

    def test_findUnsecuredUppercase_AllUpperSecuredCap(self):
        entryString = getStringEntry({FIELD_TITLE: 'WORD {A}SSOCIATION'})
        key2goldChars = {DEFAULT_KEY: [1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]}
        key2unsecuredChars = nanny.findUnsecuredUppercase(parse(entryString), field="title")
        self.assertEqual(key2unsecuredChars, key2goldChars)


class TestBadPageNumbers(TestCase):
    def test_fixBadPageNumbers_range_correct(self):
        bad_range = '153--176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_space(self):
        bad_range = '153 -- 176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_morespace(self):
        bad_range = '153   --   176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_1hyphen(self):
        bad_range = '153-176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_3hyphens(self):
        bad_range = '153---176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_4hyphens(self):
        bad_range = '153----176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_endash(self):
        bad_range = '153–176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))

    def test_fixBadPageNumbers_range_emdash(self):
        bad_range = '153—176'
        good_range = '153--176'
        self.assertEqual(good_range, fixer.fixBadPageNumbers(bad_range))


class TestBadNames(TestCase):
    # todo: Add more edge cases outlined by https://nwalsh.com/tex/texhelp/bibtx-23.html
    @staticmethod
    def getEntries4Name(nameStrings, field):
        entryDicts = [{field: name} for name in nameStrings]
        entriesString = getStringEntries(entryDicts)
        entries = parse(entriesString)
        return entries

    def assertEmpty(self, collection):
        if type(collection) == dict:
            self.assertEqual({}, collection)
        elif type(collection) == OrderedDict:
            self.assertEqual(OrderedDict(), collection)
        else:
            assert len(collection) == 0

    def test_findAllCapsName_basicName(self):
        entries = self.getEntries4Name(['Mickey Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_basicTwoNames(self):
        entries = self.getEntries4Name(['Mickey Mouse and Minie Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_basicNameAndOthers(self):
        entries = self.getEntries4Name(['Mickey Mouse and others'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_basicTwoNamesAndOthers(self):
        entries = self.getEntries4Name(['Mickey Mouse and Minie Mouse and others'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_FullNameAllCaps(self):
        entries = self.getEntries4Name(['MICKEY MOUSE'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEqual(entrykey2CapsNames,
                         {'foobar0': [algo.Name(first='MICKEY', von='', last='MOUSE', jr='')]})

    def test_findAllCapsName_LastnameAllCaps(self):
        entries = self.getEntries4Name(['Mickey MOUSE'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEqual(entrykey2CapsNames,
                         {'foobar0': [algo.Name(first='Mickey', von='', last='MOUSE', jr='')]})

    def test_findAllCapsName_FirstnameAllCaps(self):
        entries = self.getEntries4Name(['MICKEY Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEqual(entrykey2CapsNames,
                         {'foobar0': [algo.Name(first='MICKEY', von='', last='Mouse', jr='')]})

    def test_findAllCapsName_FirstnameIsInitial(self):
        entries = self.getEntries4Name(['M. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_FirstnameIsInitialNoperiod(self):
        entries = self.getEntries4Name(['M Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_MiddlenameInitial(self):
        entries = self.getEntries4Name(['Mickey D. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_MiddlenameInitialNoperiod(self):
        entries = self.getEntries4Name(['Mickey D Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_MiddlenameTwoInitialsSpaced(self):
        entries = self.getEntries4Name(['Mickey D. R. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_MiddlenameTwoInitialsNospace(self):
        entries = self.getEntries4Name(['Mickey D.R. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_MiddlenameTwoInitialsNoperiod(self):
        entries = self.getEntries4Name(['Mickey D R Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    @expectedFailure
    def test_findAllCapsName_MiddlenameTwoInitialsNoperiodNospace(self):
        entries = self.getEntries4Name(['Mickey D.R Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    @expectedFailure
    def test_findAllCapsName_MiddlenameTwoInitialsOneperiodNospace(self):
        entries = self.getEntries4Name(['Mickey DR Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_TwoInitialsSpaced(self):
        entries = self.getEntries4Name(['M. D. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_ThreeInitialsSpaced(self):
        entries = self.getEntries4Name(['M. D. R. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_TwoInitialsNospace(self):
        entries = self.getEntries4Name(['M.D. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_ThreeInitialsNospace(self):
        entries = self.getEntries4Name(['M.D.R. Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_TwoInitialsNoperiods(self):
        entries = self.getEntries4Name(['M D Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_ThreeInitialsNoperiods(self):
        entries = self.getEntries4Name(['M D R Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    @expectedFailure
    def test_findAllCapsName_TwoInitialsNoperiodNospace(self):
        entries = self.getEntries4Name(['MD Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    @expectedFailure
    def test_findAllCapsName_ThreeInitialsNoperiodNospace(self):
        entries = self.getEntries4Name(['MDR Mouse'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_LastnameNumerals(self):
        entries = self.getEntries4Name(['Mickey Mouse III', 'Mickey Mouse VI', 'Mickey Mouse IX', 'Mickey Mouse X'],
                                       FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_JuniorBasic(self):
        entries = self.getEntries4Name(['Mickey D. Mouse Jr.'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_JuniorCommaSeparated(self):
        entries = self.getEntries4Name(['Mouse, Jr., Mickey D.'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_NameSpecialchar(self):
        entries = self.getEntries4Name(['M{\\\'i}ckey Mo{\\"u}se'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_findAllCapsName_NameSecured(self):
        entries = self.getEntries4Name(['{ACME Unlimited}'], FIELD_AUTHOR)
        entrykey2CapsNames = nanny.findAllCapsName(entries, FIELD_AUTHOR)
        self.assertEmpty(entrykey2CapsNames)

    def test_fixNames_BasicName(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_FormatBasic(self):
        input_entries = self.getEntries4Name(['Mickey Mouse'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_ControlSequenceBibTeX(self):
        input_entries = self.getEntries4Name([r'M{\u o}{\"u}{\v s}e, M{\'i}{\c c}key'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_ControlSequenceLaTeXBraces(self):
        input_entries = self.getEntries4Name([r'M\u{o}\"{u}\v{s}e, M\'{i}\c{c}key'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name([r'M{\u o}{\"u}{\v s}e, M{\'i}{\c c}key'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_ControlSequenceLaTeXDirect(self):
        input_entries = self.getEntries4Name([r'M\u o\"u\v se, M\'i\c ckey'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name([r'M{\u o}{\"u}{\v s}e, M{\'i}{\c c}key'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_ControlSequenceLaTeXEmptybraces(self):
        input_entries = self.getEntries4Name([r'M\u{}ou\v{}se, Mi\c{}ckey'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name([r'M{\u o}u{\v s}e, Mi{\c c}key'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_ControlSequenceUnicode(self):
        input_entries = self.getEntries4Name(['Mŏüše, Míçkey'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name([r'M{\u o}{\"u}{\v s}e, M{\'i}{\c c}key'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FirstnameIsInitial(self):
        input_entries = self.getEntries4Name(['Mouse, M.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_FirstnameIsInitialNoperiod(self):
        input_entries = self.getEntries4Name(['Mouse, M'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_MiddlenameInitial(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_MiddlenameInitialNoperiod(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey D'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_TwoInitialsSpaced(self):
        input_entries = self.getEntries4Name(['Mouse, M. D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_ThreeInitialsSpaced(self):
        input_entries = self.getEntries4Name(['Mouse, M. D. R.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_TwoInitialsNospace(self):
        input_entries = self.getEntries4Name(['Mouse, M.D.'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_ThreeInitialsNospace(self):
        input_entries = self.getEntries4Name(['Mouse, M.D.R.'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D. R.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_TwoInitialsNoperiod(self):
        input_entries = self.getEntries4Name(['Mouse, M D'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_ThreeInitialsNoperiod(self):
        input_entries = self.getEntries4Name(['Mouse, M D R'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D. R.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    @expectedFailure
    def test_fixNames_TwoInitialsNoperiodNospace(self):
        input_entries = self.getEntries4Name(['Mouse, MD'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    @expectedFailure
    def test_fixNames_ThreeInitialsNoperiodNospace(self):
        input_entries = self.getEntries4Name(['Mouse, MDR'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D. R.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_TwoInitialsOneperiodNospace(self):
        input_entries = self.getEntries4Name(['Mouse, M.D'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    @expectedFailure
    def test_fixNames_TwoInitialsNoperiodsNospace_notAllCaps(self):
        input_entries = self.getEntries4Name(['Mouse, MD'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    @expectedFailure
    def test_fixNames_ThreeInitialsNoperiodsNospace_notAllCaps(self):
        input_entries = self.getEntries4Name(['Mouse, MDR'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, M. D. R.'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    @expectedFailure
    def test_fixNames_ThreeUSDepartmentInitials(self):
        input_entries = self.getEntries4Name(['U.S. Department of Increased Entertainment'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_FullnameAllCaps(self):
        input_entries = self.getEntries4Name(['MOUSE, MICKEY'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_FirstnameTwochars_noVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, MD'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, MD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_FirstnameThreecharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, MDR'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, MDR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_MiddlenameTwocharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, MICKEY MD'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey MD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_MiddlenameThreecharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, MICKEY MDR'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey MDR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_FirstnameTwocharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, AD'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, AD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_FirstnameThreecharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, ADR'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, ADR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_MiddlenameTwocharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, MICKEY AD'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey AD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_MiddlenameThreecharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['MOUSE, MICKEY ADR'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey ADR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FirstnameAllCaps(self):
        input_entries = self.getEntries4Name(['Mouse, MICKEY'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FirstnameTwocharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['Mouse, MD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_FirstnameThreecharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['Mouse, MDR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_MiddlenameTwocharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey MD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_MiddlenameThreecharAllCaps_noVowel(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey MDR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_FirstnameTwocharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['Mouse, AD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_FirstnameThreecharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['Mouse, ADR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_MiddlenameTwocharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey AD'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_MiddlenameThreecharAllCaps_withVowel(self):
        input_entries = self.getEntries4Name(['Mouse, Mickey ADR'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    def test_fixNames_LastnameAllCaps(self):
        input_entries = self.getEntries4Name(['MOUSE, Mickey'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_LastnameNumerals(self):
        input_entries = self.getEntries4Name(['Mouse III, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    @expectedFailure
    def test_fixNames_LastnameNumerals_BadFormat(self):
        input_entries = self.getEntries4Name(['Mickey Mouse III'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse III, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_FullnameAllCaps_LastnameNumerals(self):
        input_entries = self.getEntries4Name(['MOUSE III, MICKEY'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse III, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    @expectedFailure
    def test_fixNames_FullnameAllCaps_LastnameNumerals_BadFormat(self):
        input_entries = self.getEntries4Name(['MICKEY MOUSE III'], FIELD_AUTHOR)
        xpect_entries = self.getEntries4Name(['Mouse III, Mickey'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEqual(xpect_entries, fixed_entries)

    def test_fixNames_OrganisationAllCaps_Escaped(self):
        input_entries = self.getEntries4Name(['{DOG Project}'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)

    @expectedFailure
    def test_fixNames_OrganisationAllCaps_notEscaped(self):
        input_entries = self.getEntries4Name(['DOG Project'], FIELD_AUTHOR)
        fixed_entries = fixer.fixNames(input_entries, fixer.ChangeLogger())
        self.assertEmpty(fixed_entries)
