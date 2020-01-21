.PHONY:	build push dev

PREFIX = hub.bccvl.org.au/silvereye
IMAGE = silvereye_wps_demo
TAG ?= 0.0.6
VOLUMES = -v $(PWD)/pywps.cfg:/etc/silvereye/pywps.cfg
VOLUMES += -v $(PWD)/development.ini:/etc/silvereye/wps.ini
VOLUMES += -v $(PWD):/silvereye_wps_demos
VOLUMES += -v $(PWD)/../pywps:/pywps
VOLUMES += -v $(PWD)/../birdy:/birdy
PORTS = -p 6543:6543

build:
	docker build -t $(PREFIX)/$(IMAGE):$(TAG) .

dev:
	docker run --rm -it $(PORTS) $(VOLUMES) $(PREFIX)/$(IMAGE):$(TAG) bash

push:
	docker push $(PREFIX)/$(IMAGE):$(TAG)

run:
	docker run --rm -it $(PORTS) $(VOLUMES) $(PREFIX)/$(IMAGE):$(TAG)
