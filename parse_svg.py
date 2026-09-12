import xml.etree.ElementTree as ET
import re

tree = ET.parse('public/mockups/Macbook_Mock.svg')
root = tree.getroot()
print("SVG size:", root.attrib['width'], "x", root.attrib['height'])
