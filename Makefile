
BUILDDIR      = _build
JB_IMAGE      = craigwillis/jupyter-book
TROV_VERSION  = 0.1

.PHONY: clean jb-image docs

clean:
	rm -rf $(BUILDDIR)

jb-image:
	docker build -t $(JB_IMAGE) .

docs:
	docker run -it --rm  -v `pwd`:/src $(JB_IMAGE) jupyter-book build --all .
