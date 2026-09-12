import os
import glob
import re

files = glob.glob('src/lib/i18n/*.ts')
for f in files:
    if f.endswith('index.ts') or f.endswith('languages.selfcheck.ts'):
        continue
    with open(f, 'r') as file:
        content = file.read()
    
    # We want to add "look.bgScale": "Wallpaper scale", after "look.darkness": "..."
    # To keep it simple, just add it before "config.appearance.desc"
    target = '"config.appearance.desc"'
    replacement = '"look.bgScale": "Wallpaper scale",\n  "config.appearance.desc"'
    
    if target in content and '"look.bgScale"' not in content:
        content = content.replace(target, replacement)
        with open(f, 'w') as file:
            file.write(content)
        print(f"Patched {f}")
