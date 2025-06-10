
pages_url    := https://the-ai-alliance.github.io/open-trusted-data-initiative/
docs_dir     := docs
site_dir     := ${docs_dir}/_site
clean_dirs   := ${site_dir} ${docs_dir}/.sass-cache

# Environment variables
MAKEFLAGS            = -w  # --warn-undefined-variables
MAKEFLAGS_RECURSIVE ?= # --print-directory (only useful for recursive makes...)
UNAME               ?= $(shell uname)
ARCHITECTURE        ?= $(shell uname -m)

# Override when running `make view-local` using e.g., `JEKYLL_PORT=8000 make view-local`
JEKYLL_PORT         ?= 4000

# Used for version tagging release and other build artifacts.
GIT_HASH            ?= $(shell git show --pretty="%H" --abbrev-commit |head -1)
TIMESTAMP           ?= $(shell date +"%Y-%m-%d")

# For the static catalog generation.
STATIC_CATALOG_VERBOSE      ?= 1
STATIC_CATALOG_DIR          ?= static-catalog
STATIC_CATALOG_BIN_DIR      ?= ${STATIC_CATALOG_DIR}/src/scripts
STATIC_CATALOG_DATA_DIR     ?= ${STATIC_CATALOG_DIR}/data
STATIC_CATALOG_MARKDOWN_DIR ?= ${STATIC_CATALOG_DIR}/markdown
STATIC_CATALOG_SUFFIX       ?= processed/${TIMESTAMP}
STATIC_CATEGORIES_FILE      ?= ${STATIC_CATALOG_DATA_DIR}/data/reference/keyword-categories.json

PARQUET_SNAPSHOT_TIMESTAMP  ?= 2025-06-05
STATIC_CATALOG_DATA_PARQUET_DIR     ?= ${STATIC_CATALOG_DATA_DIR}/parquet/${PARQUET_SNAPSHOT_TIMESTAMP}
STATIC_CATALOG_DATA_JSON_TEMP_DIR   ?= ${STATIC_CATALOG_DATA_DIR}/json/temp/${TIMESTAMP}
STATIC_CATALOG_DATA_JSON_ERRORS_DIR ?= ${STATIC_CATALOG_DATA_DIR}/json/errors/${TIMESTAMP}
STATIC_CATALOG_DATA_JSON_FINAL_DIR  ?= ${STATIC_CATALOG_DATA_DIR}/json/processed/${TIMESTAMP}
STATIC_CATALOG_MARKDOWN_FINAL_DIR   ?= ${STATIC_CATALOG_DIR}/markdown/processed/${TIMESTAMP}

define help_message
Quick help for open-trusted-data-initiative make process.

make all                # Clean and locally view the website.
						# DOES NOT BUILD ANYTHING ELSE!
make clean              # Remove built artifacts, etc.
make view-pages         # View the published GitHub pages in a browser.
make view-local         # View the pages locally (requires Jekyll).
                        # Tip: "JEKYLL_PORT=8000 make view-local" uses port 8000 instead of 4000!

Tasks for building and deploying the static catalog.

make catalog            # Makes "catalog-clean", "catalog-build" and "catalog-install".
make catalog-build      # Process files from the initial parquet files through to catalog sections
						# based on the defined categories and topics in static-catalog/data/reference/keyword-categories.json.
						# The catalog files created are written to static-catalog/markdown/processed/YYYY-MM-DD and
                        # static-catalog/data/json/processed/YYYY-MM-DD.
make catalog-json       # Same as "make catalog", but only builds the JSON files.
make catalog-markdown   # Same as "make catalog", but only builds the Markdown files.
make catalog-clean      # Deletes all static-catalog/markdown/processed/YYYY-MM-DD and
                        # static-catalog/data/json/processed/YYYY-MM-DD directories.
make catalog-install    # Copies the catalog files created by "catalog-build" to "_docs" locations.

Miscellaneous tasks for help, debugging, setup, etc.

make help               # Prints this output.
make print-info         # Print the current values of some make and env. variables.
make setup-jekyll       # Install Jekyll. Make sure Ruby is installed. 
                        # (Only needed for local viewing of the document.)
make run-jekyll         # Used by "view-local"; assumes everything is already built.
                        # Tip: "JEKYLL_PORT=8000 make run-jekyll" uses port 8000 instead of 4000!
endef

define missing_shell_command_error_message
is needed by ${PWD}/Makefile. Try 'make help' and look at the README.
endef

ifndef docs_dir
$(error ERROR: There is no ${docs_dir} directory!)
endif

define gem-error-message

ERROR: Did the gem command fail with a message like this?
ERROR: 	 "You don't have write permissions for the /Library/Ruby/Gems/2.6.0 directory."
ERROR: To run the "gem install ..." command for the MacOS default ruby installation requires "sudo".
ERROR: Instead, use Homebrew (https://brew.sh) to install ruby and make sure "/usr/local/.../bin/gem"
ERROR: is on your PATH before "user/bin/gem".
ERROR:
ERROR: Or did the gem command fail with a message like this?
ERROR:   Bundler found conflicting requirements for the RubyGems version:
ERROR:     In Gemfile:
ERROR:       foo-bar (>= 3.0.0) was resolved to 3.0.0, which depends on
ERROR:         RubyGems (>= 3.3.22)
ERROR:   
ERROR:     Current RubyGems version:
ERROR:       RubyGems (= 3.3.11)
ERROR: In this case, try "brew upgrade ruby" to get a newer version.

endef

define bundle-error-message

ERROR: Did the bundle command fail with a message like this?
ERROR: 	 "/usr/local/opt/ruby/bin/bundle:25:in `load': cannot load such file -- /usr/local/lib/ruby/gems/3.1.0/gems/bundler-X.Y.Z/exe/bundle (LoadError)"
ERROR: Check that the /usr/local/lib/ruby/gems/3.1.0/gems/bundler-X.Y.Z directory actually exists. 
ERROR: If not, try running the clean-jekyll command first:
ERROR:   make clean-jekyll setup-jekyll
ERROR: Answer "y" (yes) to the prompts and ignore any warnings that you can't uninstall a "default" gem.

endef

define missing_ruby_gem_or_command_error_message
is needed by ${PWD}/Makefile. Try "gem install ..."
endef

define ruby_and_gem_required_message
'ruby' and 'gem' are required. See ruby-lang.org for installation instructions.
endef

define gem_required_message
Ruby's 'gem' is required. See ruby-lang.org for installation instructions.
endef


.PHONY: all view-pages view-local clean help 
.PHONY: setup-jekyll run-jekyll

all:: clean view-local

help::
	$(info ${help_message})
	@echo

print-info:
	@echo "GitHub Pages URL:    ${pages_url}"
	@echo "current dir:         ${PWD}"
	@echo "docs dir:            ${docs_dir}"
	@echo "site dir:            ${site_dir}"
	@echo "clean dirs:          ${clean_dirs} (deleted by 'make clean')"
	@echo
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

clean::
	rm -rf ${clean_dirs} 

view-pages::
	@python -m webbrowser "${pages_url}" || \
		(echo "ERROR: I could not open the GitHub Pages URL. Try ⌘-click or ^-click on this URL instead:" && \
		 echo "ERROR:   ${pages_url}" && exit 1 )

view-local:: setup-jekyll run-jekyll

# Passing --baseurl '' allows us to use `localhost:4000` rather than require
# `localhost:4000/The-AI-Alliance/open-trusted-data-initiative` when running locally.
run-jekyll: clean
	@echo
	@echo "Once you see the http://127.0.0.1:${JEKYLL_PORT}/ URL printed, open it with command+click..."
	@echo
	cd ${docs_dir} && bundle exec jekyll serve --port ${JEKYLL_PORT} --baseurl '' --incremental || ( echo "ERROR: Failed to run Jekyll. Try running 'make setup-jekyll'." && exit 1 )

setup-jekyll:: ruby-installed-check bundle-ruby-command-check
	@echo "Updating Ruby gems required for local viewing of the docs, including jekyll."
	gem install jekyll bundler jemoji || ${MAKE} gem-error
	bundle install || ${MAKE} bundle-error
	bundle update html-pipeline || ${MAKE} bundle-error

ruby-installed-check:
	@command -v ruby > /dev/null || \
		( echo "ERROR: ${ruby_and_gem_required_message}" && exit 1 )
	@command -v gem  > /dev/null || \
		( echo "ERROR: ${gem_required_message}" && exit 1 )

.PHONY: catalog catalog-build catalog-data-prep catalog-json catalog-markdown catalog-clean catalog-install

catalog:: catalog-clean catalog-data-prep catalog-build catalog-install

catalog-clean::
	@echo "Cleaning targets under static-catalog, not docs. The docs files are cleaned by catalog-install."
	rm -rf ${STATIC_CATALOG_DATA_JSON_TEMP_DIR}
	rm -rf ${STATIC_CATALOG_DATA_JSON_ERRORS_DIR}
	rm -rf ${STATIC_CATALOG_DATA_JSON_FINAL_DIR}
	rm -rf ${STATIC_CATALOG_MARKDOWN_FINAL_DIR}

catalog-data-prep::
	${STATIC_CATALOG_BIN_DIR}/parquet-to-json.py --verbose ${STATIC_CATALOG_VERBOSE} \
		--input ${STATIC_CATALOG_DATA_PARQUET_DIR} \
		--output ${STATIC_CATALOG_DATA_JSON_TEMP_DIR} \
		--errors ${STATIC_CATALOG_DATA_JSON_ERRORS_DIR}

catalog-build::
	${STATIC_CATALOG_BIN_DIR}/write-category-files.py --verbose ${STATIC_CATALOG_VERBOSE} \
		--cat-file ${STATIC_CATEGORIES_FILE} \
		--json-dir ${STATIC_CATALOG_DATA_PARQUET_DIR} \
		--markdown-dir ${STATIC_CATALOG_DATA_JSON_TEMP_DIR}
catalog-json::
	${STATIC_CATALOG_BIN_DIR}/write-category-files.py --verbose ${STATIC_CATALOG_VERBOSE} \
		--no-markdown \
		--cat-file ${STATIC_CATEGORIES_FILE} \
		--json-dir ${STATIC_CATALOG_DATA_PARQUET_DIR}
catalog-markdown::
	${STATIC_CATALOG_BIN_DIR}/write-category-files.py --verbose ${STATIC_CATALOG_VERBOSE} \
		--no-json \
		--cat-file ${STATIC_CATEGORIES_FILE} \
		--markdown-dir ${STATIC_CATALOG_DATA_JSON_TEMP_DIR}

catalog-install::
	${STATIC_CATALOG_BIN_DIR}/copy-files-to-docs.sh --verbose ${STATIC_CATALOG_VERBOSE}


%-error:
	$(error ${${@}-message})

%-ruby-command-check:
	@command -v ${@:%-ruby-command-check=%} > /dev/null || \
		( echo "ERROR: Ruby command/gem ${@:%-ruby-command-check=%} ${missing_ruby_gem_or_command_error_message}" && \
			exit 1 )

%-shell-command-check:
	@command -v ${@:%-shell-command-check=%} > /dev/null || \
		( echo "ERROR: shell command ${@:%-shell-command-check=%} ${missing_shell_command_error_message}" && \
			exit 1 )
