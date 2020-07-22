from xml.etree import ElementTree

response = '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <soap:Body>
      <GetStartEndPointResponse xmlns="http://www.etis.fskab.se/v1.0/ETISws">
         <GetStartEndPointResult>
            <Code>0</Code>
            <Message />
            <StartPoints>
               <Point>
                  <Id>545</Id>
                  <Name>Get Me</Name>
                  <Type>sometype</Type>
                  <X>333</X>
                  <Y>222</Y>
               </Point>
               <Point>
                  <Id>634</Id>
                  <Name>Get me too</Name>
                  <Type>sometype</Type>
                  <X>555</X>
                  <Y>777</Y>
               </Point>
            </StartPoints>
         </GetStartEndPointResult>
      </GetStartEndPointResponse>
   </soap:Body>
</soap:Envelope>'''

# define namespace mappings to use as shorthand below
namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'a': 'http://www.etis.fskab.se/v1.0/ETISws',
}
dom = ElementTree.fromstring(response)

# reference the namespace mappings here by `<name>:`
names = dom.findall(
    './soap:Body'
    '/a:GetStartEndPointResponse'
    '/a:GetStartEndPointResult'
    '/a:StartPoints'
    '/a:Point'
    '/a:Name',
    namespaces,
)
print(names)
for name in names:
    print(name.text)
