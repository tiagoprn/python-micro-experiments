#reference: http://pybit.es/download-xml-file.html

import requests

URL = "http://insert.your/feed/here.xml"

response = requests.get(URL)
with open('feed.xml', 'wb') as file:  # the b in wb is important here, otherwise you'll have "bytes" related errors 
    file.write(response.content)  # the content option allows you to dump the entire XML file (as is) into your own local XML file
