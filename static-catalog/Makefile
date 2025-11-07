
# Environment variables
MAKEFLAGS            = -w  # --warn-undefined-variables
MAKEFLAGS_RECURSIVE ?= # --print-directory (only useful for recursive makes...)
UNAME               ?= $(shell uname)
ARCHITECTURE        ?= $(shell uname -m)

# Set this to "" here on the command line if you don't use `uv`:
UV_RUN              ?= uv run

# Used for version tagging release and other build artifacts.
GIT_HASH            ?= $(shell git show --pretty="%H" --abbrev-commit |head -1)
TIMESTAMP           ?= $(shell date +"%Y-%m-%d")

DOCS_DIR            ?= ../docs

# For the static catalog generation.
CATALOG_VERBOSE      ?= 2
CATALOG_DIR          ?= .
CATALOG_BIN_DIR      ?= ${CATALOG_DIR}/src/scripts
CATALOG_DATA_DIR     ?= ${CATALOG_DIR}/data
CATALOG_MARKDOWN_DIR ?= ${CATALOG_DIR}/markdown
CATALOG_SUFFIX       ?= processed/${TIMESTAMP}
CATEGORIES_FILE      ?= ${CATALOG_DATA_DIR}/reference/keyword-categories.json
PARQUET_SNAPSHOT_TIMESTAMP  ?= ${TIMESTAMP}

CATALOG_DATA_PARQUET_DIR     ?= ${CATALOG_DATA_DIR}/parquet/${PARQUET_SNAPSHOT_TIMESTAMP}
CATALOG_DATA_JSON_TEMP_DIR   ?= ${CATALOG_DATA_DIR}/json/temp/${TIMESTAMP}
CATALOG_DATA_JSON_ERRORS_DIR ?= ${CATALOG_DATA_DIR}/json/errors/${TIMESTAMP}
CATALOG_DATA_JSON_FINAL_DIR  ?= ${CATALOG_DATA_DIR}/json/processed/${TIMESTAMP}
CATALOG_MARKDOWN_FINAL_DIR   ?= ${CATALOG_DIR}/markdown/processed/${TIMESTAMP}
CATALOG_DUCKDB_FILE          ?= ${CATALOG_DATA_DIR}/croissant.duckdb
CATALOG_DATA_LICENSES_REF    ?= ${CATALOG_DATA_DIR}/reference/all_licenses.json
CATALOG_DATA_ISO_LANGS_REF   ?= ${CATALOG_DATA_DIR}/reference/ISO-639-1-language.json
CATALOG_DOCS_JS_DIR          ?= ${DOCS_DIR}/files/data/catalog
CATALOG_DOCS_MARKDOWN_DIR    ?= ${DOCS_DIR}

define help_message
Quick help for "${CATALOG_DIR}" tasks for open-trusted-data-initiative.

Tasks for building and deploying the static catalog.

make catalog             # Makes "catalog-clean", "catalog-data-prep", "catalog-duckdb-load",
                         # "catalog-build" and "catalog-install".
make catalog-clean       # Deletes all generated files under ${CATALOG_DIR}/markdown and
                         # ${CATALOG_DIR}/data/json/ for YYYY-MM-DD.
make catalog-data-prep   # Convert the raw parquet files into JSON
make catalog-duckdb-load # Load the JSON into DuckDB tables.
make catalog-build       # Uses the DuckDB tables to create markdown and JavaScript files for the
                         # website catalog,  based on the defined categories and topics in 
                         #   ${CATALOG_DIR}/data/reference/keyword-categories.json.
                         # The catalog files created are written to 
                         #   ${CATALOG_DIR}/markdown/processed/YYYY-MM-DD and
                         #   ${CATALOG_DIR}/data/json/processed/YYYY-MM-DD.
make catalog-json        # Same as "catalog-build", but only builds the JSON files.
make catalog-markdown    # Same as "catalog-build", but only builds the Markdown files.
make catalog-install     # Copies the catalog files created by "catalog-build" to the 
                         # "${DOCS_DIR}" locations for rendering the catalog.

If the parquet file snapshot is older than today's date, use
  PARQUET_SNAPSHOT_TIMESTAMP=YYYY-MM-DD make ...
The processed files will still be written to directories using
today's date, i.e., the date the processing was actually done, while
using PARQUET_SNAPSHOT_TIMESTAMP to specify the date of the raw data
snapshot. However, if you don't care to have the two separate timestamps,
just use the following to define all times consistently, including the
date of the raw capture:
  TIMESTAMP=YYYY-MM-DD make ...

Miscellaneous tasks for help, debugging, setup, etc.

make all                # Same as "make catalog".
make help               # Prints this output.
make print-info         # Print the current values of some make and env. variables.
endef

define missing_shell_command_error_message
is needed by ${PWD}/Makefile. Try 'make help' and look at the README.
endef

.PHONY: all help catalog

all: catalog
clean:: catalog-clean

help::
	$(info ${help_message})
	@echo

print-info:
	@echo "current dir:         ${PWD}"
	@echo "GIT_HASH:            ${GIT_HASH}"
	@echo "TIMESTAMP:           ${TIMESTAMP}"
	@echo "MAKEFLAGS:           ${MAKEFLAGS}"
	@echo "MAKEFLAGS_RECURSIVE: ${MAKEFLAGS_RECURSIVE}"
	@echo "UNAME:               ${UNAME}"
	@echo "ARCHITECTURE:        ${ARCHITECTURE}"
	@echo "GIT_HASH:            ${GIT_HASH}"
	@echo "JEKYLL_PORT:         ${JEKYLL_PORT}"
	@echo
	@echo "CATEGORIES_FILE:             ${CATEGORIES_FILE}"
	@echo "CATALOG_DATA_PARQUET_DIR:    ${CATALOG_DATA_PARQUET_DIR}"
	@echo "CATALOG_DATA_JSON_TEMP_DIR:  ${CATALOG_DATA_JSON_TEMP_DIR}"
	@echo "CATALOG_DATA_JSON_FINAL_DIR: ${CATALOG_DATA_JSON_FINAL_DIR}"
	@echo "CATALOG_MARKDOWN_FINAL_DIR:  ${CATALOG_MARKDOWN_FINAL_DIR}"
	@echo "CATALOG_DUCKDB_FILE:         ${CATALOG_DUCKDB_FILE}"
	@echo "CATALOG_DATA_LICENSES_REF:   ${CATALOG_DATA_LICENSES_REF}"
	@echo "CATALOG_DATA_ISO_LANGS_REF:  ${CATALOG_DATA_ISO_LANGS_REF}"
	@echo "CATALOG_DOCS_JS_DIR:         ${CATALOG_DOCS_JS_DIR}"
	@echo "CATALOG_DOCS_MARKDOWN_DIR:   ${CATALOG_DOCS_MARKDOWN_DIR}"


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
		--errors  ${CATALOG_DATA_JSON_ERRORS_DIR}

catalog-duckdb-load:: catalog-clean-db-file
	${UV_RUN} ${CATALOG_BIN_DIR}/load-into-duckdb.py \
		--verbose   ${CATALOG_VERBOSE} \
		--db-file   ${CATALOG_DUCKDB_FILE} \
		--input     ${CATALOG_DATA_JSON_TEMP_DIR}/* \
		--licenses  ${CATALOG_DATA_LICENSES_REF} \
		--iso-langs ${CATALOG_DATA_ISO_LANGS_REF}

catalog-build::
	${UV_RUN} ${CATALOG_BIN_DIR}/write-category-files.py \
		--verbose      ${CATALOG_VERBOSE} \
		--db-file      ${CATALOG_DUCKDB_FILE} \
		--cat-file     ${CATEGORIES_FILE} \
		--json-dir     ${CATALOG_DATA_JSON_FINAL_DIR} \
		--markdown-dir ${CATALOG_MARKDOWN_FINAL_DIR}
catalog-build-json::
	${UV_RUN} ${CATALOG_BIN_DIR}/write-category-files.py \
		--no-markdown \
		--verbose      ${CATALOG_VERBOSE} \
		--db-file      ${CATALOG_DUCKDB_FILE} \
		--cat-file     ${CATEGORIES_FILE} \
		--json-dir     ${CATALOG_DATA_JSON_FINAL_DIR}
catalog-build-markdown::
	${UV_RUN} ${CATALOG_BIN_DIR}/write-category-files.py \
		--no-json \
		--verbose      ${CATALOG_VERBOSE} \
		--db-file      ${CATALOG_DUCKDB_FILE} \
		--cat-file     ${CATEGORIES_FILE} \
		--markdown-dir ${CATALOG_MARKDOWN_FINAL_DIR}

catalog-install::
	${CATALOG_BIN_DIR}/copy-files-to-docs.sh \
		--verbose ${CATALOG_VERBOSE} \
		--js-source ${CATALOG_DATA_JSON_FINAL_DIR} \
		--md-source ${CATALOG_MARKDOWN_FINAL_DIR} \
		--js-target ${CATALOG_DOCS_JS_DIR} \
		--md-target ${CATALOG_DOCS_MARKDOWN_DIR}

%-error:
	$(error ${${@}-message})

%-shell-command-check:
	@command -v ${@:%-shell-command-check=%} > /dev/null || \
		( echo "ERROR: shell command ${@:%-shell-command-check=%} ${missing_shell_command_error_message}" && \
			exit 1 )
