# BibTexNanny

BibTexNanny is a tool to check the consistency of BibTex files, fix common mistakes and generate simplified versions of a bibliography.


# BibTex Parser

BibTexNanny uses [biblib](https://github.com/aclements/biblib) to parse and generate BibTex files.

The following fixes and changes should be made to _biblib_:

- [x] Add BibDesk-compatibility mode for BibTex output
- [ ] Fix issues with loading bad month information
	- _Can't replicate issue anymore, not sure what changed._
- [x] Add ability to handle duplicate keys
- [ ] Prevent BibTex Parser from dropping metadata and comment lines
	- [x] BibTexNanny internal work-around
- [ ] When names are parsed, curly braces need to be handled correctly


# BibTex file consistency checker

- [ ] Find **duplicates**
	- [ ] Duplicate keys
		- _added biblib work-around to load files with duplicate keys._
	- [x] Duplicate paper titles
		- [ ] Grade badness of duplicate by how much of the rest matches
		- [ ] Consider cases where duplicates might be acceptable
			- [x] Pairs of entries for presentation and paper (what is the entry type for the presentation).
				- _Allow users to define entry types that should be ignored when looking for duplicate titles. This way you can for example model presentations as _`@misc`_ entries and have them be ignored_
			- [ ] Pre-print and published version of paper.
			- [ ] Author who actually named different papers differently (in what cases would this happen?)
			- [ ] Different editions of a book.
			- [ ] Possibly paper and extended version of it as journal article.
- [x] Warnings for **missing fields**
	- [x] Optional warning for optional fields
- [x] **Tex-Unicode conversion**
	- [x] LaTeX to Unicode conversion
		- [ ] Fix loosing curly braces
	- [x] Unicode to BibTeX conversion
		- [ ] Check if URLs require special handling
- [ ] Warnings for **bad formatting**
	- [ ] Warning for non-standard entry type
	- [ ] Warning for fields whose value has no curly braces, but is not a known macro
	- [x] Warnings for non-secured capitalisation in name field
	- [ ] Warnings for unnecessary curly braces
		- [ ] Curly braces are not only for uppercase characters but also for encoding special characters, e.g. `\'{e}` to get `é`
		- [ ] Allow user preference for wrapping characters or whole words.
		- [ ] _What is the difference between single and double braces?_
	- [x] Warnings for badly formatted in page numbers
	- [ ] Find badly formatted names (author and editor fields)
		- [x] All-caps names
		- [ ] Bad use of latex commands
		- [x] Missing spaces between initials
		- [ ] Other bad formattings
	- [ ] Warning for all-caps texts
	- [ ] Notice bad months
	- [ ] Check if desired key format is followed (see _entry key format_)
- [ ] Warnings for **inconsistent formatting**
	- [ ] Different names for **conferences** (see _dictionary of conference names_)
	- [ ] **Name** formatting
		- [x] Names or parts of names written in all caps (`MICKEY MOUSE` or `Mickey MOUSE`)
			- [ ] Identify when an all-caps name part is actually intials written without period or whitespace
		- [x] Name initials
			- [x] Initial written without period (`Mickey D Mouse`)
			- [x] Multiple initials written without whitespace (`Mickey A.B. Mouse`)
			- [ ] Multiple initials written without periods or whitespace (`Mickey AD Mouse`)
			- [ ] Warning when first names are only initials
			- [ ] Warning when only some names of a paper are full and some have initials
	- [ ] **Location** names
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
- [ ] **Infer full names**
	- [x] Infer full name form of initials when the full name is used elsewhere
	- [ ] Infer proper non-ASCII spelling of a name when is it used elsewhere
- [ ] **Fix inconstistent fields**
	- [ ] Replace **conference** name variations with main name (see _dictionary of conference names_)
	- [ ] Expand **name initials** to full names
		- [x] Infer full name form of initials when the full name is used elsewhere
		- [ ] Infer proper non-ASCII spelling of a name when is it used elsewhere
	- [ ] Make **locations** more informative (City, [State], Country)
		- [ ] Add missing country
		- [ ] Add missing city
		- [ ] Add state (USA only)
		- [x] Extend state initials to full state name
	- [ ] Have consistent file order
- [ ] **Fix** **formatting**
	- [x] Replace non-ASCII characters in keys
	- [x] Add wraps around capitalised characters in name field
		- [ ] Add option to wrap entire words instead of only the capitalised characters
	- [ ] Remove unnecessary {}-wraps
	- [x] Fix badly formatted page numbers
	- [ ] Fix all-caps text (but not single all caps words)
		- [ ] Separate handling for names
	- [ ] Fix bad but understandable **months** (e.g. numbers)
	- [ ] Correct handling for **escaped sequences**
			- [ ] Escaped by curly braces
			- [ ] Escaped by math mode
	- [ ] **Name** formatting
		- [x] Change format of name to non-ambiguous "Last, First" format
		- [ ] Fix special character formatting
			- [x] Use consistent braces format (e.g. write `{\"o}` instead of  `\"{o}`)
			- [x] Replace latex commands (e.g. replace `\textasciicaron{}e` with `{e}`)
		- [x] Fix all-caps names (`MICKEY MOUSE` or `Mickey MOUSE`)
		- [x] Fix initials format
			- [x] Initials must be followed by a period
			- [x] Multiple initials must be separated by spaces
		- [ ] Test if text starts with "and"
- [ ] **Rename entry keys**
	- [ ] Provide a format to specify the desired key names
	- [ ] Key format might differ for different entry types.
	- [ ] Key format should consist of only ASCII characters
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

- [ ] There might already be an open source system for standardising BibTex keys. This is also used by Zotero. Gotra check that out.


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
3. LastnameYEARkeyword
4. LastnameYEARdisambig
5. lastname_keyword_year
6. TITLEWORD
7. LastnameYEAR or KEYWORD


### How to choose format

1. Number of hardcoded options
	- Easy to implement, little flexibility
2. RegEx
	- Easy to implement, flexible, but limited functionality (can't check other fields)
	- Actually, if you use named groups, you could use those names to trigger additional checks for them.
3. Custom format
	- Lots of work to implement, full functionality, probably quite flexible


# Field Inference

- [ ] **article**: journal + year + volume => month
- [ ] **article**: journal + year + month => volume
- [ ] **book**: booktitle + year +volume/number => **inbook**: author, editor,publisher, series, edition, month, publisher
- [ ] **book**: booktitle + year +volume/number => **incollection:** editor, publisher, series, edition, month, publisher
- [ ] **conference**: booktitle + year => address, month, editor, organization, publisher
- [ ] **inbook**: title + year => address, month, editor, publisher
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
