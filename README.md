# BibTexNanny

BibTexNanny is a tool to check the consistency of BibTex files, fix common mistakes and generate simplified versions of a bibliography.


# BibTex Parser

BibTexNanny uses [biblib](https://github.com/aclements/biblib) to parse and generate BibTex files.

The following fixes and changes should be made to _biblib_:

- [x] Add BibDesk-compatibility mode for BibTex output
- [ ] Fix issues with loading bad month information
	- _Can't replicate anymore, not sure what changed._
- [ ] Add ability to handle duplicate keys
- [ ] Prevent BibTex Parser from dropping metadata and comment lines
	- [x] BibTexNanny internal work-around

# BibTex file consistency checker

- [ ] Find **duplicates**
	- [ ] Duplicate keys
		- _Currently not possible because biblib won't load files with duplicate keys._
	- [x] Duplicate paper titles
		- [ ] Grade badness of duplicate by how much of the rest matches
- [x] Warnings for **missing fields**
	- [ ] Optional warning for (specific/all) optional fields
- [ ] Warnings for **bad formatting**
	- [x] Warnings for non-secured capitalisation in name field
	- [ ] Warnings for unnecessary {}-wraps
		- Curly braces are not only for uppercase characters but also for encoding special characters, e.g. \'{e} to get é
	- [x] Warnings for badly formatted in page numbers
	- [ ] Warning for all-caps texts
	- [ ] Notice bad months
	- [ ] Check if desired key format is followed
- [ ] Warnings for **inconsistent formatting**
	- [ ] Different names for conferences (see _dictionary of conference names_)
	- [ ] Name initials formatting
	- [ ] Location names
	- [ ] Inferrable information for conferences/journals is inconsistent
- [ ] Allow limiting search to citations found in aux file

# BibTex Fixer

- [x] **Infer fields from other entries**
	- [ ] **Basic inference functionality**
	- [ ] Add more inferrable fields (see _Field Inference_)
	- [ ] Add functionality for mapping information across types (e.g. from _proceeding_ to _inproceedings_)
- [ ] **Fix inconstistent fields**
	- [ ] Replace conference name variations with main name (see _dictionary of conference names_)
	- [ ] Expand name initials to full names
	- [ ] Make locations more informative (City, [State], Country)
		- [ ] Add missing country
		- [ ] Add missing city
		- [ ] Add state (always or only USA?)
		- [ ] Extend state initials to full state name
	- [ ] Have consistent file order
- [ ] **Fix** **formatting**
	- [x] Add wraps around capitalised characters in name field
	- [ ] Remove unnecessary {}-wraps
	- [x] Fix badly formatted page numbers
	- [ ] Fix all-caps text (but not single all caps words)
	- [ ] Fix bad but understandable months (e.g. numbers)
- [ ] **Multi-bibliography merger**
	- [ ] Identify entries that are the same
		- [ ] Option 1: Same key
		- [ ] Option 2: Match on major fields (e.g. name plus authors?)
	- [ ] Merge
		- [ ] Identical fields are accepted
		- [ ] Fields available in only one version are accepted
		- [ ] Fields that clash cause user prompt or trigger other fixer functions

# BibTex simplifier

- [ ] Simplify **conference names**
	- [ ] Use _dictionary of conference names_
	- [ ] allow regex or sed replacement
- [ ] Simplify **Names**
	- [ ] Turn full first names into initials
	- [ ] Turn full middle names into initials
- [ ] Simplify **Locations**
	- [ ] Drop entirely
	- [ ] Drop city
	- [ ] Drop state
	- [ ] Shorten state to initials
	- [ ] Copy location to address (even though technically it is incorrect)

# Auxiliary


## **Dictionary of conference names**

- [ ] Allow full name, name variation, short name
- [ ] Names should allow for number placeholder
- [ ] How to link regularly named conferences with years where they were held in conjunction with something?
- [ ] **Additional script** to suggest possible name variations

## **Key formatting**


### Relevant factors for key formatting

- [ ] First author last name
	- [ ] capitalised
	- [ ] lower caps
- [ ] Year
- [ ] Word from Title
	- [ ] capitalised
	- [ ] lower caps
	- [ ] all caps
- [ ] Disambiguating characters
	- [ ] lowercase a,b,c

### Common formats

1. lastnameYEAR
2. LastnameYEAR
3. LastnameYEARtitleword
4. LastnameYEARdisambig
5. TITLEWORD
6. LastnameYEAR or TITLEWORD

### How to choose format

1. Number of hardcoded options
	- Easy to implement, little flexibility
2. RegEx
	- Easy to implement, flexible, but limited functionality (can't check other fields)
	- Actually, if you use named groups, you could use those names to trigger additional checks for them.
3. Custom format
	- Lots of work to implement, full functionality, probably quite flexible

# Field Inference

- [ ] **author**: journal + year + volume => month
- [ ] **author**: journal + year + month => volume
- [ ] **book**: booktitle + year +volume/number => **inbook**: author, editor,publisher, series, edition, month, publisher
- [ ] **book**: booktitle + year +volume/number => **incollection:** editor, publisher, series, edition, month, publisher
- [ ] **conference**: booktitle + year => address, month, editor, organization, publisher
- [ ] **incbook**: title + year => address, month, editor, publisher
- [x] **incollection**: booktitle + year => address, month, editor, publisher
- [x] i**nproceedings**: booktitle + year => address, month, editor, organization, publisher
- [ ] **proceedings**: booktitle + year => i**nproceedings: **address, month, editor, organization, publisher
- [ ] If proceedings title contains an index (e.g. "Proceedings of the 5th Conference on Examples") we can infer year and all other pieces of information from it.

# BibTexNanny Input Parameters


## Input methods

- [x] Use Python's _configparser_, which allows INI-like config files

## Internal processing

1. ~~Dict~~
	- Straightforward, but need to keep the key strings straight
2. Custom object with lots of boolean fields
	- More design effort, but probably more flexible
	- Should have different class for each Nanny component
		- As the tasks overlap considerably, there should be a NannyConfig superclass and inherriting classes for the components.
		- Accessing config info should be done via functions, not fields, to allow custom processing of the stored information

## Required states for custom variables


### Consistency checker

- [x] True _(check value)_
- [x] False _(don't check value)_

### Fixer

- [x] True/Autofix/Auto _(autofix value)_
- [x] Tryfix/Try _(autofix if trivial, otherwise prompt to fix)_
- [x] Promptfix/Prompt _(Prompt to fix)_
- [x] False _(don't check value)_

### Consistency + Fixer

How information for both scripts can be given in the same config file

- [x] Single value for both (_Try_ and _Prompt_ are treated as _True_)
- [x] ~~Tuple: False,Tryfix (CONSISTENCY,FIXER)~~
- [x] ~~Variables for only one of the two configs, e.g. _duplicateKeys-consistency_~~
- [x] Different sections for giving instructions for both or just either

### Simplifier

Should have separate config files.

- [ ] Blacklist: List fields that should be removed
- [ ] Whitelist List only the fields that are wanted
- [ ] Variables for conversion functions

# ============================================================


# Interface


## Good way to **set parameters**?

1. Argument calls
	- set list of **wanted fields** (if None, all are wanted)
	- Set list of **unwanted fields** (optional)
2. Config files
	- allows for templates
	- More complex to set up
3. Prompts during processing, asking for user decisions
	- Could also be used to auto-generate config files

# External information files


## LaTeX style files

- **.bst:** BibTex format file (difficult to parse)
- **.sty:** LaTeX style file (can this contain the bst info?)
- **.cls:** LaTeX class file (can this contain the bst info?)

## LaTeX temp files

- **.aux:** Lists citations and labels
	- Single line to parse: `\citation{citationlabel}`

## BibTexNanny files

- Dictionary of conference names
- Style config file
- Tool config files
	- Consistency checker config file
	- Fixer config file
	- Simplifier config file

# BibTex field requirements

We need to be able to check the following aspects for fields:

- What **type of entry** are we looking at?
- What are the **generally required** and optional fields for this entry?
	- This bit can be hardcoded as it is always true for all BibTex files
	- Look up BibTex documentation to determine these values
- For a particular **bibliography type**, which are the required and optional fields, which fields are ignored?
	- Easy solution: Manually create a config file that lists fields as mandatory, optional and ignored
		- Requires config file design
	- Better solution: Load style files to automatically extract this kind of information.
		- Are there python tools that can load sty and cls files for us?
- Design a **config file** that allows users to set which info they want to drop and which they need enforced
	- List by entry type
		- Allow defining fields for more than one entry type at once
	- Define fields as mandatory, optional, unused and maybe as hidden
- **Three layer approach**:
	1. In-built BibTex entry definitions
	2. Config file for bibliography style requirements
	3. Config file for simplification requirements

# People working on related tools

- [Titus von der Malsburg](https://github.com/tmalsburg/helm-bibtex)
- [Marten van Schijndel](https://github.com/vansky/bibfile_cleaner)
	- [Dave's fork](https://github.com/dmhowcroft/bibfile_cleaner)



# Wikipedia BibTex Information

The following information is taken from the [Wikipedia BibTex article](https://en.wikipedia.org/wiki/BibTeX).


# Entry types

A BibTeX database can contain the following types of entries:


### article

An article from a journal or magazine.

_Required fields:_ author, title, journal, year, volume

_Optional fields:_ number, pages, month, note, key


### book

A book with an explicit publisher.

_Required fields:_ author/editor, title, publisher, year

_Optional fields:_ volume/number, series, address, edition, month, note, key, url


### booklet

A work that is printed and bound, but without a named publisher or sponsoring institution.

_Required fields:_ title

_Optional fields:_ author, howpublished, address, month, year, note, key


### conference

The same as inproceedings, included for [Scribe](https://en.wikipedia.org/wiki/Scribe_(markup_language)) compatibility.


### inbook

A part of a book, usually untitled. May be a chapter (or section, etc.) and/or a range of pages.

_Required fields:_ author/editor, title, chapter/pages, publisher, year

_Optional fields:_ volume/number, series, type, address, edition, month, note, key


### incollection

A part of a book having its own title.

_Required fields:_ author, title, booktitle, publisher, year

_Optional fields:_ editor, volume/number, series, type, chapter, pages, address, edition, month, note, key


### inproceedings

An article in a conference proceedings.

_Required fields:_ author, title, booktitle, year

_Optional fields:_ editor, volume/number, series, pages, address, month, organization, publisher, note, key


### manual

Technical documentation.

_Required fields:_ title

_Optional fields:_ author, organization, address, edition, month, year, note, key


### mastersthesis

A [Master's](https://en.wikipedia.org/wiki/Master%27s_degree) [thesis](https://en.wikipedia.org/wiki/Thesis).

_Required fields:_ author, title, school, year

Optional fields: type, address, month, note, key


### misc

For use when nothing else fits.

_Required fields:_ none

_Optional fields:_ author, title, howpublished, month, year, note, key


### phdthesis

A [Ph.D.](https://en.wikipedia.org/wiki/Doctor_of_Philosophy) thesis.

_Required fields:_ author, title, school, year

_Optional fields:_ type, address, month, note, key


### proceedings

The proceedings of a conference.

_Required fields:_ title, year

_Optional fields_: editor, volume/number, series, address, month, publisher, organization, note, key


### techreport

A report published by a school or other institution, usually numbered within a series.

_Required fields:_ author, title, institution, year

_Optional fields:_ type, number, address, month, note, key


### unpublished

A document having an author and title, but not formally published.

_Required fields: _author, title, note

_Optional fields:_ month, year, key


# 


# Field types

A BibTeX entry can contain various types of fields. The following types are recognized by the default bibliography styles; some third-party styles may accept additional ones:


### address

Publisher's address (usually just the city, but can be the full address for lesser-known publishers)


### annote

An annotation for annotated bibliography styles (not typical)


### author

The name(s) of the author(s) (in the case of more than one author, separated by and)


### booktitle

The title of the book, if only part of it is being cited


### chapter

The chapter number


### crossref

The key of the cross-referenced entry


### edition

The edition of a book, long form (such as "First" or "Second")


### editor

The name(s) of the editor(s)


### howpublished

How it was published, if the publishing method is nonstandard


### institution

The institution that was involved in the publishing, but not necessarily the publisher


### journal

The journal or magazine the work was published in


### key

A hidden field used for specifying or overriding the alphabetical order of entries (when the "author" and "editor" fields are missing). Note that this is very different from the key (mentioned just after this list) that is used to cite or cross-reference the entry.


### month

The month of publication (or, if unpublished, the month of creation)


### note

Miscellaneous extra information


### number

The "(issue) number" of a journal, magazine, or tech-report, if applicable. (Most publications have a "volume", but no "number" field.)


### organization

The conference sponsor


### pages

Page numbers, separated either by commas or double-hyphens.


### publisher

The publisher's name


### school

The school where the thesis was written


### series

The series of books the book was published in (e.g. "[The Hardy Boys](https://en.wikipedia.org/wiki/The_Hardy_Boys)" or "[Lecture Notes in Computer Science](https://en.wikipedia.org/wiki/Lecture_Notes_in_Computer_Science)")


### title

The title of the work


### type

The field overriding the default type of publication (e.g. "Research Note" for techreport, "{PhD} dissertation" for phdthesis, "Section" for inbook/incollection)


### volume

The volume of a journal or multi-volume book


### year

The year of publication (or, if unpublished, the year of creation)

In addition, each entry contains a key (Bibtexkey) that is used to cite or cross-reference the entry. This key is the first item in a BibTeX entry, and is not part of any field.

