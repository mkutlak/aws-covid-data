PYTHON_SCRIPT=covid_scraper.py
PYTHON=python
ZIP_FILE=${PYTHON}.zip
RQS=requirements.txt

all: zip
.PHONY: all

${PYTHON}:
	@echo "Installing Python for Lambda layer."
	@mkdir -p "${PYTHON}"
	@cp "${PYTHON_SCRIPT}" "${PYTHON}"
	@echo "Requirements:" && cat "./${RQS}" ; echo
	pip3 install -Iq -t "${PYTHON}" -r "./${RQS}"

${ZIP_FILE}: ${PYTHON}
	@echo "Zipping the Python layer for Lambda."
	zip -qr "${ZIP_FILE}" "${PYTHON}"

zip: ${ZIP_FILE} clean-env

clean-env:
	@echo "Cleaning python cache."
	@rm --recursive --force "./${PYTHON}/*.dist-info" "./${PYTHON}/__pycache__"

clean:
	@echo "Cleaning python resources."
	@rm -rf "./${PYTHON}" "${ZIP_FILE}"
	@echo "Removed."
