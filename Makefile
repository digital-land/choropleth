index.html: lpa.svg demo.py var/organisation.csv
	python3 demo.py > $@

lpa.svg: var/lpa.svg Makefile svgo.js
	node_modules/svgo/bin/svgo var/lpa.svg --config svgo.js -o $@

var/lpa.svg:  var/lpa.geojson Makefile
	svgis draw var/lpa.geojson --id-field reference --crs EPSG:3857 --scale 2000 -o $@

var/lpa.geojson: var/lpa-uk.geojson filter.py
	python3 filter.py < var/lpa-uk.geojson > $@

# uses ONS version, for now
# move to use the planning.data.gov.uk dataset, with historical areas
var/lpa-uk.geojson:
	@mkdir -p var
	curl -qfsL "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Planning_Authorities_April_2023_Boundaries_UK_BUC/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson" > $@

init::
	pip install -r requirements.txt
	npm install svgo

clobber::
	rm -f lpa.svg

# local copy of organsiation datapackage
var/organisation.csv:
	@mkdir -p var/
	curl -qfs "https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv" > $@
