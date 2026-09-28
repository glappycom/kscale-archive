scads := $(patsubst %.py,out/%.stl,$(wildcard *.scad))
pys := $(patsubst %.py,out/%.stl,$(wildcard *.py))

ALL: $(pys) $(scads)

out/%.scad : %.py
	mkdir -p out
	python3 $< > $@

out/%.scad: %.2dpy
	mkdir -p out 
	python3 $< > $@

out/%.stl : %.scad
	mkdir -p out
	openscad -o $@ $<

out/%.stl : out/%.scad
	mkdir -p out
	openscad -o $@ $<

%.dxf: %.scad
	openscad -o $@ $<

out/%.pdf: %.scad
	mkdir -p out 
	openscad -o $@ $<

clean: 
	rm -f $(pys) $(scads) $(py2ds)
