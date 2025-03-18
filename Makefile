.PRECIOUS: var/cache/%

SVGS=\
	 local-planning-authority.svg

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

# build SVG from dataset
%.svg: var/%.svg Makefile svgo.js
	node_modules/svgo/bin/svgo $< --config svgo.js -o $@

var/%.svg:  var/simplified/%.geojson
	@mkdir -p $(dir $@)
	svgis draw $< --id-field reference --crs EPSG:3857 --scale 2000 -o $@

var/filtered/%.geojson: var/simplified/%.geojson
	@mkdir -p $(dir $@)
	python3 bin/filter.py < $< > $@

var/simplified/%.geojson: var/cache/%.geojson
	@mkdir -p $(dir $@)
	ogr2ogr -simplify 0.01 $@ $<

# download organisations
var/cache/organisation.csv:
	@mkdir -p $(dir $@)
	curl -qfs "https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv" > $@

# download dataset
var/cache/%.geojson:
	@mkdir -p $(dir $@)
	curl -qfsL "https://files.planning.data.gov.uk/dataset/$(notdir $@)" > $@
