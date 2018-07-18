# Based on the unicode-to-latex dict of Benjamin Wohlwend: https://gist.github.com/beniwohli/798549
unicode2bibtex = {
    ##### Simple TeX-to-Unicode replacements
    ### Active characters
    '\u00A0': '~',
    ### chardefs from plain.tex
    '%': '{\\%}',
    '&': '{\\&}',
    '#': '{\\#}',
    '$': '{\\$}',
    'ß': '{\\ss}',
    'æ': '{\\ae}',
    'œ': '{\\oe}',
    'ø': '{\\o}',
    'Æ': '{\\AE}',
    'Œ': '{\\OE}',
    'Ø': '{\\O}',
    'ı': '{\\i}',
    'ȷ': '{\\j}',
    'å': '{\\aa}',
    'Å': '{\\AA}',
    'ł': '{\\l}',
    'Ł': '{\\L}',
    ### Other defs from plain.tex
    '_': '{\\_}',
    '†': '{\\dag}',
    '‡': '{\\ddag}',
    '§': '{\\S}',
    '¶': '{\\P}',
    ##### TeX accent control sequences to Unicode combining characters
    ### Accents defined in plain.tex
    ## \`
    "\u00C0": "{\\`A}",
    "\u00E0": "{\\`a}",
    "\u00C8": "{\\`E}",
    "\u00E8": "{\\`e}",
    "\u00CC": "{\\`I}",
    "\u00EC": "{\\`i}",
    "\u00D2": "{\\`O}",
    "\u00F2": "{\\`o}",
    "\u00D9": "{\\`U}",
    "\u00F9": "{\\`u}",
    "\u0300": "\\`{}",
    ## \'
    "\u00C1": "{\\'A}",
    "\u0386": "{\\'}A",
    "\u00E1": "{\\'a}",
    "\u0106": "{\\'C}",
    "\u0107": "{\\'c}",
    "\u00C9": "{\\'E}",
    "\u0388": "{\\'}E",
    "\u00E9": "{\\'e}",
    "\u01F5": "{\\'g}",
    "\u0389": "{\\'}H",
    "\u00CD": "{\\'I}",
    "\u038A": "{\\'}I",
    "\u00ED": "{\\'i}",
    "\u0139": "{\\'L}",
    "\u013A": "{\\'l}",
    "\u0143": "{\\'N}",
    "\u0144": "{\\'n}",
    "\u1e3E": "{\\'M}",
    "\u1e3F": "{\\'m}",
    "\u00D3": "{\\'O}",
    "\u038C": "{\\'}O",
    "\u03CC": "{\\'o}",
    "\u00F3": "{\\'o}",
    "\u0154": "{\\'R}",
    "\u0155": "{\\'r}",
    "\u015A": "{\\'S}",
    "\u015B": "{\\'s}",
    "\u00DA": "{\\'U}",
    "\u00FA": "{\\'u}",
    "\u00DD": "{\\'Y}",
    "\u00FD": "{\\'y}",
    "\u0179": "{\\'Z}",
    "\u017A": "{\\'z}",
    # "\u03AC": "\\'{$\\alpha$}",
    # "\u0403": "\\cyrchar{\\'\\CYRG}",
    # "\u040C": "\\cyrchar{\\'\\CYRK}",
    # "\u0453": "\\cyrchar{\\'\\cyrg}",
    # "\u045C": "\\cyrchar{\\'\\cyrk}",
    ## \v
    "\u01cd": "{\\vA}",
    "\u01ce": "{\\va}",
    "\u010C": "{\\vC}",
    "\u010D": "{\\vc}",
    "\u010E": "{\\vD}",
    "\u010F": "{\\vd}",
    "\u011A": "{\\vE}",
    "\u011B": "{\\ve}",
    "\u01Cf": "{\\vI}",
    "\u01D0": "{\\vI}",
    "\u01E9": "{\\vK}",
    "\u01E8": "{\\vk}",
    "\u013D": "{\\vL}",
    "\u013E": "{\\vl}",
    "\u0147": "{\\vN}",
    "\u0148": "{\\vn}",
    "\u01D1": "{\\vO}",
    "\u01D2": "{\\vO}",
    "\u0158": "{\\vR}",
    "\u0159": "{\\vr}",
    "\u0160": "{\\vS}",
    "\u0161": "{\\vs}",
    "\u0164": "{\\vT}",
    "\u0165": "{\\vt}",
    "\u01D3": "{\\vU}",
    "\u01D4": "{\\vU}",
    "\u017D": "{\\vZ}",
    "\u017E": "{\\vz}",
    ## \u
    "\u0102": "{\\uA}",
    "\u0103": "{\\ua}",
    "\u0114": "{\\uE}",
    "\u0115": "{\\ue}",
    "\u011E": "{\\uG}",
    "\u011F": "{\\ug}",
    "\u012C": "{\\uI}",
    "\u012D": "{\\ui}",
    "\u014E": "{\\uO}",
    "\u014F": "{\\uo}",
    "\u021A": "{\\uT}",
    "\u021B": "{\\ut}",
    "\u016C": "{\\uU}",
    "\u016D": "{\\uu}",
    ## \=
    "\u0100": "{\\=A}",
    "\u0101": "{\\=a}",
    "\u0112": "{\\=E}",
    "\u0113": "{\\=e}",
    "\u012A": "{\\=I}",
    "\u012B": "{\\=i}",
    "\u014C": "{\\=O}",
    "\u014D": "{\\=o}",
    "\u016A": "{\\=U}",
    "\u016B": "{\\=u}",
    ## \^
    "\u00C2": "{\\^A}",
    "\u00E2": "{\\^a}",
    "\u0108": "{\\^C}",
    "\u0109": "{\\^c}",
    "\u00CA": "{\\^E}",
    "\u00EA": "{\\^e}",
    "\u011C": "{\\^G}",
    "\u011D": "{\\^g}",
    "\u0124": "{\\^H}",
    "\u0125": "{\\^h}",
    "\u00CE": "{\\^I}",
    "\u00EE": "{\\^i}",
    "\u0134": "{\\^J}",
    "\u0135": "{\\^j}",
    "\u00D4": "{\\^O}",
    "\u00F4": "{\\^o}",
    "\u015C": "{\\^S}",
    "\u015D": "{\\^s}",
    "\u00DB": "{\\^U}",
    "\u00FB": "{\\^u}",
    "\u0174": "{\\^W}",
    "\u0175": "{\\^w}",
    "\u0176": "{\\^Y}",
    "\u0177": "{\\^y}",
    ## \.
    "\u010A": "{\\.C}",
    "\u010B": "{\\.c}",
    "\u0116": "{\\.E}",
    "\u0117": "{\\.e}",
    "\u0120": "{\\.G}",
    "\u0121": "{\\.g}",
    "\u0130": "{\\.I}",
    "\u017B": "{\\.Z}",
    "\u017C": "{\\.z}",
    ## \H
    "\u0150": "{\\HO}",
    "\u0151": "{\\Ho}",
    "\u0170": "{\\HU}",
    "\u0171": "{\\Hu}",
    ## \~
    "\u00C3": "{\\~A}",
    "\u00E3": "{\\~a}",
    "\u0128": "{\\~I}",
    "\u0129": "{\\~i}",
    "\u00D1": "{\\~N}",
    "\u00F1": "{\\~n}",
    "\u00D5": "{\\~O}",
    "\u00F5": "{\\~o}",
    "\u0168": "{\\~U}",
    "\u0169": "{\\~u}",
    ## \"
    "\u00C4": "{\\\"A}",
    "\u00E4": "{\\\"a}",
    "\u00CB": "{\\\"E}",
    "\u00EB": "{\\\"e}",
    "\u00CF": "{\\\"I}",
    "\u00EF": "{\\\"i}",
    "\u00D6": "{\\\"O}",
    "\u00F6": "{\\\"o}",
    "\u00DC": "{\\\"U}",
    "\u00FC": "{\\\"u}",
    "\u1e84": "{\\\"W}",
    "\u1e85": "{\\\"w}",
    "\u0178": "{\\\"Y}",
    "\u00FF": "{\\\"y}",
    ## \d
    ## \b
    ## \c
    "\u0327": "{\\c}",
    "\u00C7": "{\\cC}",
    "\u00E7": "{\\cc}",
    "\u0122": "{\\cG}",
    "\u0123": "{\\cg}",
    "\u0136": "{\\cK}",
    "\u0137": "{\\ck}",
    "\u013B": "{\\cL}",
    "\u013C": "{\\cl}",
    "\u0145": "{\\cN}",
    "\u0146": "{\\cn}",
    "\u0156": "{\\cR}",
    "\u0157": "{\\cr}",
    "\u015E": "{\\cS}",
    "\u015F": "{\\cs}",
    "\u0162": "{\\cT}",
    "\u0163": "{\\ct}",
    ### Other accents that seem to be standard
    ## \r
    "\u016E": "{\\rU}",
    "\u016F": "{\\ru}",
    ## \k
    "\u0104": "{\\kA}",
    "\u0105": "{\\ka}",
    "\u0118": "{\\kE}",
    "\u0119": "{\\ke}",
    "\u012E": "{\\kI}",
    "\u012F": "{\\ki}",
    "\u0172": "{\\kU}",
    "\u0173": "{\\ku}",
}

unicodeCombiningCharacter2bibtex = {
    "\u0303": "{{\\~{}}}",
    "\u0308": "{{\\\"{}}}",
    "\u030A": "{{\\r{}}}",
    "\u030C": "{{\\v{}}}",
    "\u0306": "{{\\u{}}}",
    "\u0304": "{{\\={}}}",
    "\u0302": "{{\\^{}}}",
    "\u0307": "{{\\.{}}}",
    "\u030B": "{{\\H{}}}",
    "\u0301": "{{\\'{}}}",
}