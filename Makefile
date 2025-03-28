.NOTINTERMEDIATE:

SVGS=\
	 svg/border.svg\
	 svg/region.svg\
	 svg/local-authority-district.svg\
	 svg/national-park.svg\
	 svg/local-planning-authority.svg

POINT_DATASETS=\
	var/cache/border.csv\
	var/cache/region.csv\
	var/cache/local-authority-district.csv\
	var/cache/national-park.csv\
    var/cache/local-planning-authority.csv

all:: $(SVGS) svg/point.svg index.html

index.html: bin/demo.py var/cache/organisation.csv $(SVGS)
	python3 bin/demo.py > $@

init::
	pip install -r requirements.txt
	npm install svgo

server::
	python3 -m http.server 9000

clobber::
	rm -f index.html $(SVGS)

clean::
	rm -rf ./var

# points in England
var/point.geojson: $(POINT_DATASETS) bin/point.py var/border.geojson
	python bin/point.py $(POINT_DATASETS) > $@

# build boundary SVG from dataset
svg/%.svg: var/%.svg svgo.js
	node_modules/svgo/bin/svgo $< --config svgo.js -o $@

var/%.svg:  var/%.geojson
	@mkdir -p $(dir $@)
	svgis draw $< --id-field reference --crs EPSG:3857 --scale 2000 -o $@

var/%.geojson: var/simplified/%.geojson
	@mkdir -p $(dir $@)
	python3 bin/filter.py < $< > $@

var/simplified/%.geojson: var/cache/%.geojson
	@mkdir -p $(dir $@)
	ogr2ogr -simplify 0.001 $@ $<

# download organisations
var/cache/organisation.csv:
	@mkdir -p $(dir $@)
	curl -qfs "https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv" > $@

# download dataset
var/cache/%.csv:
	@mkdir -p $(dir $@)
	curl -qfs "https://files.planning.data.gov.uk/dataset/$(notdir $@)" > $@

var/cache/%.geojson:
	@mkdir -p $(dir $@)
	curl -qfsL "https://files.planning.data.gov.uk/dataset/$(notdir $@)" > $@
