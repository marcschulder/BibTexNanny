# BibTex Nanny

#ToDo


# BibTex Parser

- [x] Find existing parser
	- [Biblib](https://github.com/aclements/biblib) looks promissing
	- [ ] Try out parser

# BibTex file consistency checker

- [ ] Find **duplicates**
	- [ ] Duplicate keys
	- [x] Duplicate paper titles
		- [ ] Grade badness of duplicate by how much of the rest matches
- [ ] Warnings for **missing fields**
	- [ ] Optional warning for (specific/all) optional fields
- [ ] Warnings for **bad formatting**
	- [x] Warnings for non-secured capitalisation in name field
	- [ ] Warnings for unnecessary {}-wraps
	- [x] Warnings for badly formatted in page numbers
	- [ ] Warning for all-caps texts
	- [ ] Notice bad months
- [ ] Warnings for **inconsistent formatting**
	- [ ] Different names for conferences (see _dictionary of conference names_)
	- [ ] Name initials formatting
	- [ ] Location names
- [ ] Allow limiting search to citations found in aux file

# BibTex Fixer

- [ ] **Auto-add fields**
	- [ ] If conference and year match with more complete entry, add location
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

# **Dictionary of conference names**

- [ ] Allow full name, name variation, short name
- [ ] Names should allow for number placeholder
- [ ] How to link regularly named conferences with years where they were held in conjunction with something?
- [ ] **Additional script** to suggest possible name variations

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
