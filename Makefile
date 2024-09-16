index.html: lpa.svg demo.py var/organisation.csv
	python3 demo.py > $@

lpa.svg: var/lpa.svg Makefile svgo.js
	node_modules/svgo/bin/svgo var/lpa.svg --config svgo.js -o $@

var/lpa.svg:  var/lpa.geojson Makefile
	svgis draw var/lpa.geojson --id-field reference --crs EPSG:3857 --scale 2000 -o $@

var/lpa.geojson: var/lpa-eng.geojson filter.py
	python3 filter.py < var/lpa-eng.geojson > $@

var/lpa-eng.geojson: var/lpa-uk.geojson
	ogr2ogr -simplify 0.01 $@ var/lpa-uk.geojson

# uses ONS version, for now
# move to use the planning.data.gov.uk dataset, with historical areas
var/lpa-uk.geojson:
	@mkdir -p var
	curl -qfsL "https://files.planning.data.gov.uk/dataset/local-planning-authority.geojson" > $@

init::
	pip install -r requirements.txt
	npm install svgo

server::
	python3 -m http.server

clobber::
	rm -f lpa.svg

clean::
	rm -rf ./var

# local copy of organsiation datapackage
var/organisation.csv:
	@mkdir -p var/
	curl -qfs "https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv" > $@
