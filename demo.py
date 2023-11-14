#!/usr/bin/env python3

import re
import sys
import csv

lpas = {}
for row in csv.DictReader(open("var/organisation.csv")):
    lpas[row["local-planning-authority"]] = row

background = "#505a5f";
legends = [
    { "name": "black", "colour": background, "legend": "No data expected" },
    { "name": "grey", "colour": "#b1b4b6", "legend": "Project is paused" },
    { "name": "red", "colour": "#d4351c", "legend": "Data is missing" },
    { "name": "amber", "colour": "#f47738", "legend": "Data has outstanding issues" },
    { "name": "turquoise", "colour": "#28a197", "legend": "Data may be used by the project" },
    { "name": "green", "colour": "#85994b", "legend": "Data meets the standard" },
]

counts = {
    "black": 201,
    "grey": 1,
    "red": 60,
    "amber": 60,
    "turquoise": 60,
    "green": 5,
}
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
 fill: """ + background + """;
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

pattern = re.compile(r"id=\"(?P<lpa>\w+)")

with open("lpa.svg") as f:
    for line in f.readlines():
        if '<path id="E' in line:
            match = pattern.search(line)

            lpa = match.group("lpa")
            if lpa in lpas:
                org = lpas[lpa]
                name = org["name"]
                line = line.replace("/>", f"><title>{name}</title></path>")
        print(line, end="")


print('<div class="stacked-chart">')

for item in legends:
    value = counts[item["name"]]
    percent = 100 * value / total
    print(f'<div class="bar {item["name"]}" style="width:{percent:.2f}%;">{value}</div>')

print("""</div>
<ul class="key">""")

for item in legends:
    print(f'<li class="key-item {item["name"]}">{item["legend"]}</li>')

print("""</ul>
</div>
</body>
</html>""")
