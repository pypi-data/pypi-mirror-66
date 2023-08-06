import os
import json
import collections

# Gem en tabel til en fil
def to_file(entity, name_pattern="{schema}.{name}.json", folder=".", path=None):
    # Clean up empty entity tag list
    if "tags" in entity and not entity["tags"]:
        del entity["tags"]
    # Clean up empty attribtue tag lists
    for attr in entity.get("attributes", []):
        if "tags" in attr and not attr["tags"]:
            del attr["tags"]
    # If no path provided, check if the entity has a path.
    if not path:
        # If it does, use that
        if "__path" in entity:
            path = entity.pop("__path")
        # if not, come up with a default
        else:
            file_name = name_pattern.format(schema=entity["schema"], name=entity["name"])
            path = os.path.join(folder, file_name)

    with open(path, 'w') as f:
        json.dump(entity, f, indent=4)

# Hent en tabel fra en fil
def from_file(path):
    with open(path, 'rb') as f:
        entity = json.load(f, object_pairs_hook=collections.OrderedDict)
    # Add attribute list if missing
    if "attributes" not in entity:
        entity["attributes"] = []
    # Add entity tag list if missing
    if "tags" not in entity:
        entity["tags"] = []
    # Add attribute tag lists if missing
    for attr in entity["attributes"]:
        if not attr.get("tags",()):
            attr["tags"] = []
    entity["__path"] = path
    return entity
