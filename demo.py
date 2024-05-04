#!/usr/bin/env python3

import re
import sys
import csv

lpas = {}
for row in csv.DictReader(open("var/organisation.csv")):
    row["class"] = "mid-grey"
    lpas[row["local-planning-authority"]] = row

# TBD: use performance-dataset
lpas["E60000167"]["class"] = "grey"
lpas["E60000331"]["class"] = "turquoise"

legends = [
    { "name": "black", "colour": "#0b0c0c", "legend": "Unknown LPA" },
    { "name": "mid-grey", "colour": "#505a5f", "legend": "No data expected" },
    { "name": "grey", "colour": "#b1b4b6", "legend": "Project is paused" },
    { "name": "red", "colour": "#d4351c", "legend": "Data is missing" },
    { "name": "amber", "colour": "#f47738", "legend": "Data has outstanding issues" },
    { "name": "turquoise", "colour": "#28a197", "legend": "Data may be used by the project" },
    { "name": "green", "colour": "#85994b", "legend": "Data meets the standard" },
]

counts = {}
for row in legends:
    counts[row["name"]] = 0

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
    (name, colour) = (item["name"], item["colour"])
    print(f".stacked-chart .bar.{name} {{ background-color: {colour}; }}")
    print(f".key-item.{name} {{ border-color: {colour}; }}")
    print(f"svg path.{name} {{ fill: {colour}; stroke: {colour}; }}")


print("""
</style>
</head>
<body>
<div class="choropleth">
""")

re_id = re.compile(r"id=\"(?P<lpa>\w+)")

with open("lpa.svg") as f:
    for line in f.readlines():

        line = line.replace(' fill-rule="evenodd"', '')
        line = line.replace('class="polygon ', 'class="')

        match = re_id.search(line)
        if match:
            lpa = match.group("lpa")

            if lpa not in lpas:
                counts["black"] += 1
                name = lpa
                _class = "black"
            else:
                org = lpas[lpa]
                name = org["name"]
                _class = org.get("class", "white")

        if 'class="lpa"' in line:
            line = line.replace('class="lpa"/>', f'class="lpa {_class}"><title>{name}</title></path>')

        print(line, end="")


print('<div class="stacked-chart">')

for item in legends:
    value = counts[item["name"]]
    if value:
        percent = 100 * value / total
        print(f'<div class="bar {item["name"]}" style="width:{percent:.2f}%;">{value}</div>')

print("""</div>
<ul class="key">""")

for item in legends:
    value = counts[item["name"]]
    if value:
        print(f'<li class="key-item {item["name"]}">{item["legend"]}</li>')

print("""</ul>
</div>
</body>
</html>""")
