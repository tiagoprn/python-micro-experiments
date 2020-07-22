# works on python 3.6+
import operator
from collections import OrderedDict

references = {'customer': 4, 'user': 28, 'buyer': 15, 'seller': 3}

references_sorted = OrderedDict(sorted(references.items(), key=operator.itemgetter(1)))  # natural order
references_sorted_descending = OrderedDict(sorted(references.items(), key=operator.itemgetter(1), reverse=True))  # descending order

print(f'sorted in ascending order = {references_sorted}')
print(f'sorted in descending order = {references_sorted_descending}')

