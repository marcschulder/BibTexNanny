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
		- [ ] Indicate when there is a country without a city
		- [ ] Indicate when there is a city without a country
		- [ ] States missing from US locations
	- [ ] Inferrable information for conferences/journals is inconsistent
- [ ] Allow limiting search to citations found in aux file

# BibTex Fixer

- [ ] **Infer fields from other entries**
	- [x] _**Basic inference functionality**_
	- [ ] Add more inferrable fields (see _Field Inference_)
	- [ ] Add functionality for mapping information across types (e.g. from _proceeding_ to _inproceedings_)
- [ ] **Fix inconstistent fields**
	- [ ] Replace conference name variations with main name (see _dictionary of conference names_)
	- [ ] Expand name initials to full names
	- [ ] Make locations more informative (City, [State], Country)
		- [ ] Add missing country
		- [ ] Add missing city
		- [ ] Add state (USA and Canada)
		- [x] Extend state initials to full state name
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
