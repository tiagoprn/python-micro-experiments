import re

"""
IMPORTANT:
"re.search" and "re.match" are different.
They both attempt to apply a pattern to an input string.
But search attempts this at all possible starting points in the string.
Match just tries the first starting point.
So, for the sake of correctness, you should ALWAYS use re.search.
Reference: http://www.dotnetperls.com/re

More on regexes can be found at:
https://developers.google.com/edu/python/regular-expressions
"""


text = '500.99 1,500.87 8.99 0.00 1,999,999.78'

REGEX = r'[+-]?[\d]+(\,[\d]{3})*\.[\d]{2}'

print '-' * 80
print 'INPUT TEXT: ', text
print 'REGEX: ', REGEX
print 'MATCHES:'
print '-' * 80
found_items = re.finditer(REGEX, text)

if found_items:
    for item in found_items:
        item_as_str = text[item.start():item.end()]
        print item_as_str
else:
    print 'NOT FOUND'

print '/' * 80

'''
BELOW IS A MORE SIMPLIFIED WAY.
It uses a feature of python regexes called "groups", where you
sinalize between "()" on the regex the parts of it that you want returned.
As a bonus, it also supports unicode strings.
'''
regex = r'#synonym_(\w+)%(\w+)#'
string = '#synonym_brand%chevrolet#'
unicode_pattern = re.compile(regex, re.UNICODE)
found = re.findall(unicode_pattern, string.encode('utf-8'))

print 'INPUT TEXT: ', string
print 'REGEX: ', regex
print 'GROUPS FOUND: {}'.format(repr(found))

print '/' * 80

'''
NAMED GROUPS:
Below I use a regex feature called "named groups".
It can be used if you want back "chunks" of the matched string.
In the example, there are 2 groups named "thousands" and "decimals".
I can get their values on the matched string through the "groupdict()"
method from the match.
'''

value = u'Ar Condicionado Split Mini Brize Komeco 9.000 Btus Frio - 220 Volts'
regex = '(?P<thousands>[0-9]{1,3})[\\.]?(?P<decimals>[0-9]{3}) btu[s]?'
match = re.search(regex, value, re.UNICODE | re.IGNORECASE)

print 'INPUT TEXT: ', value
print 'REGEX: ', regex
print 'FULL MATCH:', match.group()
print 'DESIRED MATCH CHUNKS: '
print repr(match.groupdict())
