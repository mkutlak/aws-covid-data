PYTHON_SCRIPT=covid_scraper.py
PYTHON=python
RQS=requirements.txt

all: install clean-env zip
.PHONY: all

install:
	@echo "Installing Python for Lambda layer."
	@mkdir -p "${PYTHON}"
	@cp "${PYTHON_SCRIPT}" "${PYTHON}"
	@echo "Requirements:" && cat "./${RQS}" ; echo
	pip3 install -Iq -t "${PYTHON}" -r "./${RQS}"

zip: install clean-env
	@echo "Zipping the Python layer for Lambda."
	zip -qr "${PYTHON}.zip" "${PYTHON}"

clean-env:
	@echo "Cleaning python cache."
	@rm --recursive --force "./${PYTHON}/*.dist-info" "./${PYTHON}/__pycache__"

clean:
	@echo "Cleaning python resources."
	@rm -rf "./${PYTHON}" "${PYTHON}.zip"
	@echo "Removed."
