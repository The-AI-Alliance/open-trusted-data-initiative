# Makefile for the open-trusted-data-initiative code and GitHub pages website.


# Include all the common targets.
include .common.mk

# For the static catalog generation.
CATALOG_DIR          ?= ${SRC_DIR}/static-catalog
CATALOG_BIN_DIR      ?= ${CATALOG_DIR}/tools
CATALOG_DATA_DIR     ?= ${CATALOG_DIR}/data
CATALOG_MARKDOWN_DIR ?= ${CATALOG_DIR}/markdown
CATALOG_SUFFIX       ?= processed/${TIMESTAMP}
CATEGORIES_FILE      ?= ${CATALOG_DATA_DIR}/reference/keyword-categories.json
CATALOG_VERBOSE      ?= 2
# CATALOG_OPT_ARGS:  Empty by default; define on invocation to customize behavior,
#                    e.g., "CATALOG_OPT_ARGS=--help"
CATALOG_OPT_ARGS     ?=

PARQUET_SNAPSHOT_TIMESTAMP   ?= ${TIMESTAMP}

CATALOG_DATA_PARQUET_DIR     ?= ${CATALOG_DATA_DIR}/parquet/${PARQUET_SNAPSHOT_TIMESTAMP}
CATALOG_DATA_JSON_TEMP_DIR   ?= ${CATALOG_DATA_DIR}/json/temp/${TIMESTAMP}
CATALOG_DATA_JSON_ERRORS_DIR ?= ${CATALOG_DATA_DIR}/json/errors/${TIMESTAMP}
CATALOG_DATA_JSON_FINAL_DIR  ?= ${CATALOG_DATA_DIR}/json/processed/${TIMESTAMP}
CATALOG_MARKDOWN_FINAL_DIR   ?= ${CATALOG_DIR}/markdown/processed/${TIMESTAMP}
CATALOG_DUCKDB_FILE          ?= ${CATALOG_DATA_DIR}/croissant.duckdb
CATALOG_DATA_LICENSES_REF    ?= ${CATALOG_DATA_DIR}/reference/all_licenses.json
CATALOG_DATA_ISO_LANGS_REF   ?= ${CATALOG_DATA_DIR}/reference/ISO-639-1-language.json
CATALOG_DOCS_JS_DIR          ?= ${WEBSITE_DIR}/files/data/catalog
CATALOG_DOCS_MARKDOWN_DIR    ?= ${WEBSITE_DIR}

# Add custom help for the application here, which will be shown when the user
# types "make help".
# When you see ${CODE}${_END} without anything between them in help messages,
# it is there to make it easier to line up multi-line description comments.
# See for example the definition of help-message-general in .common.mk.

help::
	$(info ${help-custom-message})

define help-custom-message
${HIGHLIGHT}Quick help for the ${CODE}static-catalog${_END}${HIGHLIGHT}targets:${_END_BOLD}${_END}

Tasks for building and deploying the static catalog.

${CODE}make catalog${_END}             # Makes ${CODE}catalog-clean${_END}, ${CODE}catalog-data-prep${_END}", ${CODE}catalog-duckdb-load${_END}",
${CODE}${_END}                         # ${CODE}catalog-build${_END} and ${CODE}catalog-install${_END}.
${CODE}make catalog-clean${_END}       # Deletes all generated files under ${CODE}${CATALOG_DIR}/markdown${_END} and
${CODE}${_END}                         # ${CODE}${CATALOG_DIR}/data/json/${_END} for YYYY-MM-DD.
${CODE}make catalog-data-prep${_END}   # Convert the raw parquet files into JSON
${CODE}make catalog-duckdb-load${_END} # Load the JSON into DuckDB tables.
${CODE}make catalog-build${_END}       # Uses the DuckDB tables to create markdown and JavaScript files for the
${CODE}${_END}                         # website catalog,  based on the defined categories and topics in
${CODE}${_END}                         #   ${CODE}${CATALOG_DIR}/data/reference/keyword-categories.json${_END}.
${CODE}${_END}                         # The catalog files created are written to
${CODE}${_END}                         #   ${CODE}${CATALOG_DIR}/markdown/processed/YYYY-MM-DD${_END} and
${CODE}${_END}                         #   ${CODE}${CATALOG_DIR}/data/json/processed/YYYY-MM-DD${_END}.
${CODE}make catalog-json${_END}        # Same as ${CODE}catalog-build${_END}, but only builds the JSON files.
${CODE}make catalog-markdown${_END}    # Same as ${CODE}catalog-build${_END}, but only builds the Markdown files.
${CODE}make catalog-install${_END}     # Copies the catalog files created by ${CODE}catalog-build${_END} to the
${CODE}${_END}                         # ${CODE}${WEBSITE_DIR}${_END} locations for rendering the catalog.

If the parquet file snapshot is older than today's date, use
  ${CODE}PARQUET_SNAPSHOT_TIMESTAMP=YYYY-MM-DD make ...${_END}
The processed files will still be written to directories using
today's date, i.e., the date the processing was actually done, while
using ${CODE}PARQUET_SNAPSHOT_TIMESTAMP${_END} to specify the date of the raw data
snapshot. However, if you don't care to have the two separate timestamps,
just use the following to define all times consistently, including the
date of the raw capture:
  ${CODE}TIMESTAMP=YYYY-MM-DD make ...${_END}
endef

clean:: catalog-clean

print-info-custom::
	@echo
	@echo "${CODE}CATEGORIES_FILE${_END}:             ${CODE}${CATEGORIES_FILE}${_END}"
	@echo "${CODE}CATALOG_DATA_PARQUET_DIR${_END}:    ${CODE}${CATALOG_DATA_PARQUET_DIR}${_END}"
	@echo "${CODE}CATALOG_DATA_JSON_TEMP_DIR${_END}:  ${CODE}${CATALOG_DATA_JSON_TEMP_DIR}${_END}"
	@echo "${CODE}CATALOG_DATA_JSON_FINAL_DIR${_END}: ${CODE}${CATALOG_DATA_JSON_FINAL_DIR}${_END}"
	@echo "${CODE}CATALOG_MARKDOWN_FINAL_DIR${_END}:  ${CODE}${CATALOG_MARKDOWN_FINAL_DIR}${_END}"
	@echo "${CODE}CATALOG_DUCKDB_FILE${_END}:         ${CODE}${CATALOG_DUCKDB_FILE}${_END}"
	@echo "${CODE}CATALOG_DATA_LICENSES_REF${_END}:   ${CODE}${CATALOG_DATA_LICENSES_REF}${_END}"
	@echo "${CODE}CATALOG_DATA_ISO_LANGS_REF${_END}:  ${CODE}${CATALOG_DATA_ISO_LANGS_REF}${_END}"
	@echo "${CODE}CATALOG_DOCS_JS_DIR${_END}:         ${CODE}${CATALOG_DOCS_JS_DIR}${_END}"
	@echo "${CODE}CATALOG_DOCS_MARKDOWN_DIR${_END}:   ${CODE}${CATALOG_DOCS_MARKDOWN_DIR}${_END}"
	@echo


.PHONY: catalog catalog-data-prep catalog-duckdb-load catalog-build catalog-build-json catalog-build-markdown catalog-install
.PHONY: catalog-clean catalog-clean-notice catalog-clean-db-file catalog-clean-json catalog-clean-markdown

catalog:: catalog-clean catalog-data-prep catalog-duckdb-load catalog-build catalog-install

catalog-clean:: catalog-clean-notice catalog-clean-db-file catalog-clean-json catalog-clean-markdown
catalog-clean-notice::
	@echo "Cleaning targets under ${CATALOG_DIR}, not docs. The docs files are cleaned by catalog-install."
catalog-clean-json::
	rm -rf ${CATALOG_DATA_JSON_TEMP_DIR}
	rm -rf ${CATALOG_DATA_JSON_ERRORS_DIR}
	rm -rf ${CATALOG_DATA_JSON_FINAL_DIR}
catalog-clean-markdown::
	rm -rf ${CATALOG_MARKDOWN_FINAL_DIR}
catalog-clean-db-file::
	rm -f  ${CATALOG_DUCKDB_FILE}

catalog-data-prep::
	${UV_RUN} ${CATALOG_BIN_DIR}/parquet-to-json.py \
		--verbose ${CATALOG_VERBOSE} \
		--input   ${CATALOG_DATA_PARQUET_DIR} \
		--output  ${CATALOG_DATA_JSON_TEMP_DIR} \
		--errors  ${CATALOG_DATA_JSON_ERRORS_DIR} \
		${CATALOG_OPT_ARGS}

catalog-duckdb-load:: catalog-clean-db-file
	${UV_RUN} ${CATALOG_BIN_DIR}/load-into-duckdb.py \
		--verbose   ${CATALOG_VERBOSE} \
		--db-file   ${CATALOG_DUCKDB_FILE} \
		--input     ${CATALOG_DATA_JSON_TEMP_DIR}/* \
		--licenses  ${CATALOG_DATA_LICENSES_REF} \
		--iso-langs ${CATALOG_DATA_ISO_LANGS_REF} \
		${CATALOG_OPT_ARGS}

catalog-build::
	${UV_RUN} ${CATALOG_BIN_DIR}/write-category-files.py \
		--verbose      ${CATALOG_VERBOSE} \
		--db-file      ${CATALOG_DUCKDB_FILE} \
		--cat-file     ${CATEGORIES_FILE} \
		--json-dir     ${CATALOG_DATA_JSON_FINAL_DIR} \
		--markdown-dir ${CATALOG_MARKDOWN_FINAL_DIR} \
		${CATALOG_OPT_ARGS}

catalog-build-json::
	${UV_RUN} ${CATALOG_BIN_DIR}/write-category-files.py \
		--no-markdown \
		--verbose      ${CATALOG_VERBOSE} \
		--db-file      ${CATALOG_DUCKDB_FILE} \
		--cat-file     ${CATEGORIES_FILE} \
		--json-dir     ${CATALOG_DATA_JSON_FINAL_DIR} \
		${CATALOG_OPT_ARGS}

catalog-build-markdown::
	${UV_RUN} ${CATALOG_BIN_DIR}/write-category-files.py \
		--no-json \
		--verbose      ${CATALOG_VERBOSE} \
		--db-file      ${CATALOG_DUCKDB_FILE} \
		--cat-file     ${CATEGORIES_FILE} \
		--markdown-dir ${CATALOG_MARKDOWN_FINAL_DIR} \
		${CATALOG_OPT_ARGS}

catalog-install::
	${CATALOG_BIN_DIR}/copy-files-to-docs.sh \
		--verbose ${CATALOG_VERBOSE} \
		--js-source ${CATALOG_DATA_JSON_FINAL_DIR} \
		--md-source ${CATALOG_MARKDOWN_FINAL_DIR} \
		--js-target ${CATALOG_DOCS_JS_DIR} \
		--md-target ${CATALOG_DOCS_MARKDOWN_DIR} \
		${CATALOG_OPT_ARGS}

# Skip pylint, which currently doesn't pass (TODO - fix)
pylint-command:
	@echo "${skip-command-target-message}"
	@true
