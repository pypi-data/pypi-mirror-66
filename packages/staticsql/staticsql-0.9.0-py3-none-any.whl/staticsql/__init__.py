import os
import json


# Gem en tabel til en fil
def to_file(entity, name_pattern="{schema}.{name}.json", folder="."):
    file_name = name_pattern.format(schema=entity["schema"], name=entity["name"])
    path = os.path.join(folder, file_name) # Her kunne vi have brugt en anden folder
    with open(path, 'w') as f:
        json.dump(entity, f, indent=4)

# Hent en tabel fra en fil
def from_file(path):
    with open(path, 'r') as f:
        entity = json.load(f)
    return entity

