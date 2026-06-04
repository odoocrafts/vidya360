import os

BASE_DIR = '/Users/anas/Documents/Coding/Odoo/odoo19/custom_addons/Vidya360'

for root, _, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            new_content = content.replace('<tree', '<list').replace('</tree>', '</list>').replace('tree,form', 'list,form')
            
            if new_content != content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {path}")
