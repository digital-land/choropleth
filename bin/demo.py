#!/usr/bin/env python3

import re
import csv

lpas = {}
for row in csv.DictReader(open("var/cache/organisation.csv")):
    row["class"] = "none"
    lpas[row["local-planning-authority"]] = row


stroke = "#DEE0E2"

# TBD: use performance-dataset
lpas["E60000331"]["class"] = "trustworthy"
lpas["E60000168"]["class"] = "usable"
lpas["E60000173"]["class"] = "exists"
lpas["E60000169"]["class"] = "some"
lpas["E60000172"]["class"] = "none"
lpas["E60000174"]["class"] = "error"

# see https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours-in-charts/
legends = [
    { "reference": "trustworthy", "colour": "#12436D", "name": "Trustworthy data", "description": "Authorititive data with no known issues" },
    { "reference": "usable", "colour": "#28A197", "name": "Usable data", "description": "Data is usable by open digital planning" },
    { "reference": "exists", "colour": "#F46A25", "name": "Some authoritive data", "description": "Some data provided by the authorititive source" },
    { "reference": "some", "colour": "#BFC1C3", "name": "Some data", "description": "Some data is available for this area" },
    { "reference": "none", "colour": "#F8F8F8", "name": "No data", "description": "No data" },
    { "reference": "error", "colour": "#801650", "name": "Error", "description": "Unknown organisation or area" },
]

counts = {}
for row in legends:
    counts[row["reference"]] = 0

for lpa, l in lpas.items():
    counts[l["class"]] += 1

total = sum(counts.values())

print("""<!doctype html>
<html lang="en-GB">
<head>
<style>
html {
  font-family: sans-serif;
  font-size: 14px;
  color: #0b0c0c;
}
body {
  padding: 5px 10px;
}

.choropleth {
 width: 400px;
 resize: both;
}

.choropleth svg {
 width: 100%;
 fill: 	#0b0c0c;
}

.stacked-chart {
  display: flex;
  width: 99%;
  margin: 1em 0;
}

.stacked-chart .bar {
  display: flex;
  justify-content: left;
  align-items: center;
  height: 2em;
  text-indent: 1em;
  color: #ffffff;
}

ul.key {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

li.key-item {
   border-left: 16px solid;
   margin-bottom: 5px;
   padding-left: 5px;
}
""")

for item in legends:
    (reference, colour) = (item["reference"], item["colour"])
    print(f".stacked-chart .bar.{reference} {{ background-color: {colour}; color: #000 }}")
    print(f".key-item.{reference} {{ border-color: {colour}; }}")
    print(f"svg path.{reference} {{ fill: {colour}; stroke: {stroke}; }}")
print(f"svg path:hover {{ fill: #ffdd00 }}")


print("""
</style>
</head>
<body>
<div class="choropleth">
""")

re_id = re.compile(r"id=\"(?P<lpa>\w+)")

with open("svg/local-planning-authority.svg") as f:
    for line in f.readlines():

        line = line.replace(' fill-rule="evenodd"', '')
        line = line.replace('class="polygon ', 'class="')

        match = re_id.search(line)
        if match:
            lpa = match.group("lpa")

            if lpa not in lpas:
                counts["error"] += 1
                name = lpa
                _class = "error"
            else:
                org = lpas[lpa]
                name = org["name"]
                _class = org.get("class", "white")

        if 'class="local-planning-authority"' in line:
            line = line.replace('<path', f'<a href="#{lpa}"><path')
            line = line.replace('class="local-planning-authority"/>', f'class="local-planning-authority {_class}"><title>{name}</title></path></a>')

        print(line, end="")


print('<div class="stacked-chart">')

for item in legends:
    value = counts[item["reference"]]
    if value:
        percent = 100 * value / total
        print(f'<div class="bar {item["reference"]}" style="width:{percent:.2f}%;">{value}</div>')

print("""</div>
<ul class="key">""")

for item in legends:
    value = counts[item["reference"]]
    if value:
        print(f'<li class="key-item {item["reference"]}">{item["description"]}</li>')

print("""</ul>
</div>
</body>
</html>""")
