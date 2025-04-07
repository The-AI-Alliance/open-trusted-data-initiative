# Open Trusted Data Initiative README

Welcome to the AI Alliance [Open Trusted Data Initiative](https://the-ai-alliance.github.io/open-trusted-data-initiative/) (OTDI).

## Vision

OTDI is building a high-quality, trusted, and open catalog of datasets for AI LLM pre-training, fine-tuning, and domain-specific applications. These datasets are amenable to a wide variety of use cases in enterprises, governments, regulated industries, and wherever high trust in the data foundations of AI is essential.

The initiative consists of several projects:

* [Define Openness Criteria](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22dataset+requirements%22): What has to be true about a dataset in order for it to be considered truly _open_ for use? This project defines those criteria. See the [Dataset Specification](https://the-ai-alliance.github.io/open-trusted-data-initiative/dataset-requirements/) page for our evolving thinking on the minimally-sufficient criteria.
* [Data Pipelines](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22data+pipelines%22): Data pipelines implemented using tools like [DPK](https://github.com/The-AI-Alliance/dpk-alliance) are used both to validate datasets proposed for inclusion in our catalog and, eventually, to derive new datasets specialized for particular purposes. See the [How We Process Datasets](https://the-ai-alliance.github.io/open-trusted-data-initiative/our-processing/) page for more information.
* [Open Dataset Catalog](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22dataset+catalog%22): A catalog of datasets from many sources that meet our criteria for openness. See the [Dataset Catalog](https://the-ai-alliance.github.io/open-trusted-data-initiative/catalog/) page for more information.

Each of these projects welcome enthusiastic participants! Please join us!

## Using This Repo

This repo will contain the "code" for the [OTDI website](https://the-ai-alliance.github.io/open-trusted-data-initiative/), as well as the code that implements the projects for OTDI.

### About the GitHub Pages Website Published from this Repo

The website is published using [GitHub Pages](https://pages.github.com/), where the pages are written in Markdown/HTML and served using [Jekyll](https://github.com/jekyll/jekyll). We use the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) Jekyll theme.

See [GITHUB_PAGES.md](GITHUB_PAGES.md) for more information, especially for instructions on  previewing changes locally using `jekyll`.

> [!NOTE]
> All documentation is licensed under Creative Commons Attribution 4.0 International. See [LICENSE.CDLA-2.0](LICENSE.CDLA-2.0).

### Other Documentation and Code

This repo will also [host the code](code) for the projects that are part of OTDI, listed above. Eventually, as these projects grow, we may move them out to separate repos. 

Miscellaneous other documentation, not in the website, is also captured here:

* [`tools-notes`](tools-notes) - Notes on potential tool choices.
* [`data-processing-notes`](data-processing-notes) - Notes on requirements and data-specific tool choices.

## Getting Involved

We welcome contributions as PRs. Please see our [Alliance community repo](https://github.com/The-AI-Alliance/community/) for general information about contributing to any of our projects. This section provides some specific details you need to know.

In particular, see the AI Alliance [CONTRIBUTING](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md) instructions. You will need to agree with the AI Alliance [Code of Conduct](https://github.com/The-AI-Alliance/community/blob/main/CODE_OF_CONDUCT.md).

All _code_ contributions are licensed under the [Apache 2.0 LICENSE](https://github.com/The-AI-Alliance/community/blob/main/LICENSE.Apache-2.0) (which is also in this repo, [LICENSE.Apache-2.0](LICENSE.Apache-2.0)).

All _documentation_ contributions are licensed under the [Creative Commons Attribution 4.0 International](https://github.com/The-AI-Alliance/community/blob/main/LICENSE.CC-BY-4.0) (which is also in this repo, [LICENSE.CC-BY-4.0](LICENSE.CC-BY-4.0)).

All _data_ contributions are licensed under the [Community Data License Agreement - Permissive - Version 2.0](https://github.com/The-AI-Alliance/community/blob/main/LICENSE.CDLA-2.0) (which is also in this repo, [LICENSE.CDLA-2.0](LICENSE.CDLA-2.0)).

### We use the "Developer Certificate of Origin" (DCO).

> [!WARNING]
> Before you make any git commits with changes, understand what's required for DCO.

See the Alliance contributing guide [section on DCO](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#developer-certificate-of-origin) for details. In practical terms, supporting this requirement means you must use the `-s` flag with your `git commit` commands.

