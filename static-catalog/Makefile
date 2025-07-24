
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
STATIC_CATALOG_VERBOSE      ?= 1
STATIC_CATALOG_DIR          ?= .
STATIC_CATALOG_BIN_DIR      ?= ${STATIC_CATALOG_DIR}/src/scripts
STATIC_CATALOG_DATA_DIR     ?= ${STATIC_CATALOG_DIR}/data
STATIC_CATALOG_MARKDOWN_DIR ?= ${STATIC_CATALOG_DIR}/markdown
STATIC_CATALOG_SUFFIX       ?= processed/${TIMESTAMP}
STATIC_CATEGORIES_FILE      ?= ${STATIC_CATALOG_DATA_DIR}/reference/keyword-categories.json
PARQUET_SNAPSHOT_TIMESTAMP  ?= ${TIMESTAMP}

STATIC_CATALOG_DATA_PARQUET_DIR     ?= ${STATIC_CATALOG_DATA_DIR}/parquet/${PARQUET_SNAPSHOT_TIMESTAMP}
STATIC_CATALOG_DATA_JSON_TEMP_DIR   ?= ${STATIC_CATALOG_DATA_DIR}/json/temp/${TIMESTAMP}
STATIC_CATALOG_DATA_JSON_ERRORS_DIR ?= ${STATIC_CATALOG_DATA_DIR}/json/errors/${TIMESTAMP}
STATIC_CATALOG_DATA_JSON_FINAL_DIR  ?= ${STATIC_CATALOG_DATA_DIR}/json/processed/${TIMESTAMP}
STATIC_CATALOG_MARKDOWN_FINAL_DIR   ?= ${STATIC_CATALOG_DIR}/markdown/processed/${TIMESTAMP}
STATIC_CATALOG_DUCKDB_FILE          ?= ${STATIC_CATALOG_DATA_DIR}/croissant.duckdb
STATIC_CATALOG_DATA_LICENSES_REF    ?= ${STATIC_CATALOG_DATA_DIR}/reference/license-id-name-mapping.json
STATIC_CATALOG_DATA_ISO_LANGS_REF   ?= ${STATIC_CATALOG_DATA_DIR}/reference/ISO-639-1-language.json
STATIC_CATALOG_DOCS_JS_DIR          ?= ${DOCS_DIR}/files/data/catalog
STATIC_CATALOG_DOCS_MARKDOWN_DIR    ?= ${DOCS_DIR}

define help_message
Quick help for "${STATIC_CATALOG_DIR}" tasks for open-trusted-data-initiative.

Tasks for building and deploying the static catalog.

make catalog             # Makes "catalog-clean", "catalog-data-prep", "catalog-duckdb-load",
                         # "catalog-build" and "catalog-install".
make catalog-clean       # Deletes all generated files under ${STATIC_CATALOG_DIR}/markdown and
                         # ${STATIC_CATALOG_DIR}/data/json/ for YYYY-MM-DD.
make catalog-data-prep   # Convert the raw parquet files into JSON
make catalog-duckdb-load # Load the JSON into DuckDB tables.
make catalog-build       # Uses the DuckDB tables to create markdown and JavaScript files for the
                         # website catalog,  based on the defined categories and topics in 
                         #   ${STATIC_CATALOG_DIR}/data/reference/keyword-categories.json.
                         # The catalog files created are written to 
                         #   ${STATIC_CATALOG_DIR}/markdown/processed/YYYY-MM-DD and
                         #   ${STATIC_CATALOG_DIR}/data/json/processed/YYYY-MM-DD.
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
	@echo "STATIC_CATEGORIES_FILE:             ${STATIC_CATEGORIES_FILE}"
	@echo "STATIC_CATALOG_DATA_PARQUET_DIR:    ${STATIC_CATALOG_DATA_PARQUET_DIR}"
	@echo "STATIC_CATALOG_DATA_JSON_TEMP_DIR:  ${STATIC_CATALOG_DATA_JSON_TEMP_DIR}"
	@echo "STATIC_CATALOG_DATA_JSON_FINAL_DIR: ${STATIC_CATALOG_DATA_JSON_FINAL_DIR}"
	@echo "STATIC_CATALOG_MARKDOWN_FINAL_DIR:  ${STATIC_CATALOG_MARKDOWN_FINAL_DIR}"
	@echo "STATIC_CATALOG_DUCKDB_FILE:         ${STATIC_CATALOG_DUCKDB_FILE}"
	@echo "STATIC_CATALOG_DATA_LICENSES_REF:   ${STATIC_CATALOG_DATA_LICENSES_REF}"
	@echo "STATIC_CATALOG_DATA_ISO_LANGS_REF:  ${STATIC_CATALOG_DATA_ISO_LANGS_REF}"
	@echo "STATIC_CATALOG_DOCS_JS_DIR:         ${STATIC_CATALOG_DOCS_JS_DIR}"
	@echo "STATIC_CATALOG_DOCS_MARKDOWN_DIR:   ${STATIC_CATALOG_DOCS_MARKDOWN_DIR}"


.PHONY: catalog catalog-data-prep catalog-duckdb-load catalog-build catalog-build-json catalog-build-markdown catalog-install
.PHONY: catalog-clean catalog-clean-notice catalog-clean-db-file catalog-clean-json catalog-clean-markdown

catalog:: catalog-clean catalog-data-prep catalog-duckdb-load catalog-build catalog-install

catalog-clean:: catalog-clean-notice catalog-clean-db-file catalog-clean-json catalog-clean-markdown
catalog-clean-notice::
	@echo "Cleaning targets under ${STATIC_CATALOG_DIR}, not docs. The docs files are cleaned by catalog-install."
catalog-clean-json::
	rm -rf ${STATIC_CATALOG_DATA_JSON_TEMP_DIR}
	rm -rf ${STATIC_CATALOG_DATA_JSON_ERRORS_DIR}
	rm -rf ${STATIC_CATALOG_DATA_JSON_FINAL_DIR}
catalog-clean-markdown::
	rm -rf ${STATIC_CATALOG_MARKDOWN_FINAL_DIR}
catalog-clean-db-file::
	rm -f  ${STATIC_CATALOG_DUCKDB_FILE}

catalog-data-prep::
	${UV_RUN} ${STATIC_CATALOG_BIN_DIR}/parquet-to-json.py \
		--verbose ${STATIC_CATALOG_VERBOSE} \
		--input   ${STATIC_CATALOG_DATA_PARQUET_DIR} \
		--output  ${STATIC_CATALOG_DATA_JSON_TEMP_DIR} \
		--errors  ${STATIC_CATALOG_DATA_JSON_ERRORS_DIR}

catalog-duckdb-load:: catalog-clean-db-file
	${UV_RUN} ${STATIC_CATALOG_BIN_DIR}/load-into-duckdb.py \
		--verbose   ${STATIC_CATALOG_VERBOSE} \
		--db-file   ${STATIC_CATALOG_DUCKDB_FILE} \
		--input     ${STATIC_CATALOG_DATA_JSON_TEMP_DIR}/* \
		--licenses  ${STATIC_CATALOG_DATA_LICENSES_REF} \
		--iso-langs ${STATIC_CATALOG_DATA_ISO_LANGS_REF}

catalog-build::
	${UV_RUN} ${STATIC_CATALOG_BIN_DIR}/write-category-files.py \
		--verbose      ${STATIC_CATALOG_VERBOSE} \
		--db-file      ${STATIC_CATALOG_DUCKDB_FILE} \
		--cat-file     ${STATIC_CATEGORIES_FILE} \
		--json-dir     ${STATIC_CATALOG_DATA_JSON_FINAL_DIR} \
		--markdown-dir ${STATIC_CATALOG_MARKDOWN_FINAL_DIR}
catalog-build-json::
	${UV_RUN} ${STATIC_CATALOG_BIN_DIR}/write-category-files.py \
		--no-markdown \
		--verbose      ${STATIC_CATALOG_VERBOSE} \
		--db-file      ${STATIC_CATALOG_DUCKDB_FILE} \
		--cat-file     ${STATIC_CATEGORIES_FILE} \
		--json-dir     ${STATIC_CATALOG_DATA_JSON_FINAL_DIR}
catalog-build-markdown::
	${UV_RUN} ${STATIC_CATALOG_BIN_DIR}/write-category-files.py \
		--no-json \
		--verbose      ${STATIC_CATALOG_VERBOSE} \
		--db-file      ${STATIC_CATALOG_DUCKDB_FILE} \
		--cat-file     ${STATIC_CATEGORIES_FILE} \
		--markdown-dir ${STATIC_CATALOG_MARKDOWN_FINAL_DIR}

catalog-install::
	${STATIC_CATALOG_BIN_DIR}/copy-files-to-docs.sh \
		--verbose ${STATIC_CATALOG_VERBOSE} \
		--js-source ${STATIC_CATALOG_DATA_JSON_FINAL_DIR} \
		--md-source ${STATIC_CATALOG_MARKDOWN_FINAL_DIR} \
		--js-target ${STATIC_CATALOG_DOCS_JS_DIR} \
		--md-target ${STATIC_CATALOG_DOCS_MARKDOWN_DIR}

%-error:
	$(error ${${@}-message})

%-shell-command-check:
	@command -v ${@:%-shell-command-check=%} > /dev/null || \
		( echo "ERROR: shell command ${@:%-shell-command-check=%} ${missing_shell_command_error_message}" && \
			exit 1 )
