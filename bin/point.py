#!/usr/bin/env python3

import re
import sys
import simplejson as json
import csv
from decimal import Decimal


csv.field_size_limit(sys.maxsize)


def add_features(e, path):
    with open(path, 'r') as file:
        data = json.load(file)
        for f in data["features"]:
            reference = f["properties"]["reference"]
            name = f["properties"]["name"]
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


def add_points(e, path):
    for row in csv.DictReader(open(path)):
        if row["point"]:
            x, y = re.findall(r"-?(?:\.\d+|\d+(?:\.\d*)?)", row["point"])
            e["features"].append(
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [Decimal(x), Decimal(y)],
                        },
                        "properties": {
                            "name": row["name"],
                            "reference": row["reference"],
                            }
                        }
                    )



if __name__ == "__main__":
    e = {"type":"FeatureCollection", "features": []}

    add_points(e, "var/cache/local-planning-authority.csv")
    add_points(e, "var/cache/local-authority-district.csv")
    add_points(e, "var/cache/national-park.csv")
    add_points(e, "var/cache/region.csv")
    add_features(e, "var/border.geojson")

    json.dump(e, sys.stdout, indent=2, use_decimal=True)
