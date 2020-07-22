# requirement: beautifulsoup4==4.6.0

from bs4 import BeautifulSoup

xml_text = '''<?xml version="1.0"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns
:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">
    <SOAP-ENV:Body SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:NS1="urn:PINF-IPINF">
        <NS1:Response xmlns:NS2="urn:PINF">
            <NS2:Results id="1" xsi:type="NS2:Results">
                <Name xsi:type="xsd:string">John</Name>
                <Mensagem xsi:type="xsd:string">I am me.</Mensagem>
            </NS2:Results>
            <return href="#1"/>
        </NS1:Response>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''


xml_object = BeautifulSoup(xml_text)

new_node = xml_object.new_tag('response_data')
new_node.string = '{"key": "value"}'

xml_object.find('ns2:results').append(new_node)

xml_contents = str(xml_object).replace('\n', '').replace(':soap-enc', 'soap-enc')

print(xml_contents)

