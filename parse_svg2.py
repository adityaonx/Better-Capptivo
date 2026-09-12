import xml.etree.ElementTree as ET

tree = ET.parse('public/mockups/Macbook_Mock.svg')
root = tree.getroot()
namespaces = {'svg': 'http://www.w3.org/2000/svg'}

# find the rect or path that fills the screen
for elem in root.findall('.//svg:path', namespaces):
    d = elem.attrib.get('d', '')
    if 'M207 56.7962' in d and elem.attrib.get('fill') == 'white':
        print("Found white screen hole!")
        
