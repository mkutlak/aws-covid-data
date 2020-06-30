LAMBDA_SCRIPT=lambda_function.py
PYTHON_SCRIPT=covid_scraper.py
LAMBDA=lambda
PYTHON=python

all: install clean-env zip zip-lambda
.PHONY: all

install:
	mkdir -p ${PYTHON}
	cp ${PYTHON_SCRIPT} ${PYTHON}
	pip3 install -It ${PYTHON} -r ./requirements.txt

zip: install clean-env
	zip -r "${PYTHON}.zip" ${PYTHON}

zip-lambda:
	zip -r "${LAMBDA}.zip" ${LAMBDA_SCRIPT}

clean-env:
	rm --recursive --force "./${PYTHON}/*.dist-info"
	rm --recursive --force "./${PYTHON}/__pycache__"

clean:
	rm -rf ./${PYTHON} "${PYTHON}.zip" "${LAMBDA}.zip"
