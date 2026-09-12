import re

with open('public/mockups/Macbook_Mock.svg', 'r') as f:
    content = f.read()

# The screen hole path is:
# d="M207 56.7962C207 44.8901 216.652 35.2383 228.558 35.2383H1820.44C1832.35 35.2383 1842 44.8901 1842 56.7962V1097.24H207V56.7962Z" fill="white"
target = 'd="M207 56.7962C207 44.8901 216.652 35.2383 228.558 35.2383H1820.44C1832.35 35.2383 1842 44.8901 1842 56.7962V1097.24H207V56.7962Z" fill="white"'
replacement = 'd="M207 56.7962C207 44.8901 216.652 35.2383 228.558 35.2383H1820.44C1832.35 35.2383 1842 44.8901 1842 56.7962V1097.24H207V56.7962Z" fill="none"'

if target in content:
    content = content.replace(target, replacement)
    with open('public/mockups/Macbook_Mock.svg', 'w') as f:
        f.write(content)
    print("Patched SVG to make screen hole transparent!")
else:
    print("Could not find the target string in SVG.")
