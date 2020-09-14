# Filters a list of dicts to only contain the
# dicts where active=True.

elements = [
    {'spreadsheet_uid': '001', 'active': True,},
    {'spreadsheet_uid': '002', 'active': True,},
    {'spreadsheet_uid': '003', 'active': True,},
    {'spreadsheet_uid': '004', 'active': False,},
    {'spreadsheet_uid': '005', 'active': False,},
]
active_elements = list(filter(lambda d: d['active'], elements))
