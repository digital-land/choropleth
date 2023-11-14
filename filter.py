import sys
import json

uk = json.load(sys.stdin)

e = {"type":"FeatureCollection", "features": []}

for f in uk["features"]:
    reference = f["properties"]["LPA23CD"]
    name = f["properties"]["LPA23NM"]
    if reference[0] == "E":
        e["features"].append(
            {
                "type": "Feature",
                "geometry": f["geometry"],
                "properties": {
                    "name": name,
                    "reference": reference,
                }
            }
        )

json.dump(e, sys.stdout)
