# Entry Types

_The following information is taken from the [Wikipedia BibTex article](https://en.wikipedia.org/wiki/BibTeX)._

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

_Required fields:_ author, title, note

_Optional fields:_ month, year, key

