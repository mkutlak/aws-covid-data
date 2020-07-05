CONT=covid_terra
IMAGE=terralpine

all: build run
.PHONY: all

build:
	@echo "Building docker image for github.com/mkutlak/aws-covid-data.git"
	@docker build --tag "${IMAGE}" -f Dockerfile .

run:
	@echo "Starting and switching into the terralpine container."
	@docker run --name "${CONT}" -it "${IMAGE}"

clean_container:
	@echo "Removing container '${CONT}'"
	docker rm ${CONT}

clean: clean_container
	@echo "Removing image '${IMAGE}'."
	docker rmi ${IMAGE}
	@echo "Removed."
