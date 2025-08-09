---
layout: default
title: Key Contributors
nav_order: 400
has_children: false
parent: Dataset Catalog
---

# Our Key Contributors and Their Datasets

The following AI Alliance member or affiliate organizations, shown in alphabetical order, maintain open data sets that are becoming part of our catalog. See also the [Other Datasets]({{site.baseurl}}/catalog/other_datasets/) page.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

{: .note}
> **NOTE:** See also the AI Alliance's [Hugging Face organization](https://huggingface.co/aialliance){:target="aia-hf"} and the [dataset collection](https://huggingface.co/collections/aialliance/open-trusted-data-catalog-66d21b3cb66342762fb6108e){:target="aia-hf-otdi"} there, which list some datasets discussed below, as well as others that were donated or created by Alliance members.

## BrightQuery

[BrightQuery](https://brightquery.ai/){:target="bq"} ("BQ") provides proprietary financial, legal, and employment information on private and public companies derived from regulatory filings and disclosures. BQ proprietary data is used in capital markets for investment decisions, banking and insurance for KYC & credit checks, and enterprises for master data management, sales, and marketing purposes.

In addition, BQ provides public information consisting of clean and standardized statistical data from all the major government agencies and NGOs around the world, and is doing so in partnership with the source agencies. BQ public datasets will be published at [opendata.org/](https://opendata.org/){:target="od"} and cataloged in OTDI spanning all topics: economics, demographics, healthcare, crime, climate, education, sustainability, etc. See also their [documentation](https://docs.brightquery.com/index.html){:target="_blank"} about the datasets they are building. Much of the data will be tabular (i.e., structured) time series data, as well as unstructured text.

_More specific information is coming soon._

## Common Crawl Foundation

[Common Crawl Foundation](https://commoncrawl.org/){:target="ccf"} is working on tagged and filtered crawl subsets for English and other languages.

_More specific information is coming soon._

## EPFL

The [EPFL LLM team](https://huggingface.co/epfl-llm){:target="epfl-llm"} has curated a dataset to train their [Meditron](https://github.com/epfLLM/meditron){:target="meditron"} models. An open-access subset of the medical guidelines data is published on [Hugging Face](https://huggingface.co/datasets/epfl-llm/guidelines){:target="guidelines"}

See the Meditron GitHub repo [README](https://github.com/epfLLM/meditron?tab=readme-ov-file#medical-training-data){:target="meditron-readme"} for more details about the whole dataset used to train Meditron.

## IBM Research

### Social Stigma Q&A

Social Stigma Q&A is a dataset from IBM Research. From the [arXiv paper abract](http://arxiv.org/abs/2312.07492){:target="social-stigma"}:

{: .highlight}
> Current datasets for unwanted social bias auditing are limited to studying protected demographic features such as race and gender. In this work, we introduce a comprehensive benchmark that is meant to capture the amplification of social bias, via stigmas, in generative language models. Taking inspiration from social science research, we start with a documented list of 93 US-centric stigmas and curate a question-answering (QA) dataset which involves simple social situations. Our benchmark, SocialStigmaQA, contains roughly 10K prompts, with a variety of prompt styles, carefully constructed to systematically test for both social bias and model robustness. We present results for SocialStigmaQA with two open source generative language models and we find that the proportion of socially biased output ranges from 45% to 59% across a variety of decoding strategies and prompting styles. We demonstrate that the deliberate design of the templates in our benchmark (e.g., adding biasing text to the prompt or using different verbs that change the answer that indicates bias) impacts the model tendencies to generate socially biased output. Additionally, through manual evaluation, we discover problematic patterns in the generated chain-of-thought output that range from subtle bias to lack of reasoning.

For more information, see [Arxiv:2312.07492](http://arxiv.org/abs/2312.07492){:target="social-stigma"}.

### Kepler

[Kepler](https://github.com/sustainable-computing-io/kepler){:target="kepler"} ([paper](https://dl.acm.org/doi/10.1145/3604930.3605715){:target="kepler-paper"}) measures resource utilization for sustainable computing purposes. From the repo:

{: .highlight}
> Kepler (Kubernetes-based Efficient Power Level Exporter) uses eBPF to probe performance counters and other system stats, use ML models to estimate workload energy consumption based on these stats, and exports them as Prometheus metrics.

## Meta

### Data for Good at Meta

[Data for Good at Meta](https://dataforgood.facebook.com/dfg/){:target="dfg"} empowers partners with privacy-preserving data that strengthens communities and advances social issues. Data for Good is helping organizations respond to crises around the world and supporting research that advances economic opportunity.

There are 220 datasets available. See [Meta's page](https://data.humdata.org/organization/meta){:target="humdata"} at the [Humanitarian Data Exchange](https://data.humdata.org/){:target="humdata"} for the full list of datasets.

### OMol25

[OMol25](https://huggingface.co/facebook/OMol25){:target="_blank"} is an open dataset for molecules and electrolytes, possibly the largest _ab-initio_ dataset ever released in terms of compute cost and a family of Universal Model for Atoms (UMA) trained against all of the open-science datasets the team has released in the past five years (materials, catalysts, molecules, MOFs, organic crystals).

For more information, including a demo to see how it works on different materials, see the following:

* [Blog post](https://ai.meta.com/blog/meta-fair-science-new-open-source-releases/){:target="omol25-blog"}: including links to the research paper, the dataset, the trained model, and code.
* [Demo](https://facebook-fairchem-uma-demo.hf.space/){:target="omol25-demo"}
* Press coverage: [SEMAFOR](https://www.semafor.com/article/05/14/2025/meta-releases-new-data-set-ai-model-aimed-at-speeding-up-scientific-research){:target="omol25-semafor"}

## Mohamed bin Zayed University of Artificial Intelligence (MBZUAI)

Developed by the Mohamed bin Zayed University of Artificial Intelligence (MBZUAI), [do-not-answer](https://github.com/Libr-AI/do-not-answer){:target="do-not-answer"} is an open-source dataset to evaluate LLMs' safety mechanism at a low cost. The dataset is curated and filtered to consist only of prompts to which responsible language models do not answer. Besides human annotations, Do not answer also implements model-based evaluation, where a 600M fine-tuned BERT-like evaluator achieves comparable results with human and GPT-4.

## PleIAs

Domain-specific, clean datasets.

* PleIAs [website](https://pleias.fr){:target="pleias"}
* PleIAs [Hugging Face organization](https://huggingface.co/PleIAs){:target="pleias-hf"}.
* PleIAs [Collections on Hugging Face](https://huggingface.co/collections/PleIAs){:target="pleias-hf-col"}

| Name             | Description     |  URL     | Date Added |
| :--------------- | :-------------- | :------- | :--------- |
| **Common Corpus** | Largest multilingual pretraining data | [Hugging Face](https://huggingface.co/collections/PleIAs/common-corpus-6734e0f67ac3f35e44075f93){:target="common-corpus"} [paper](https://arxiv.org/abs/2506.01732){:target="_blank"} | 2024-11-04 |
| **Toxic Commons** | Tools for de-toxifying public domain data, especially multilingual and historical text data and data with OCR errors | [Hugging Face](https://huggingface.co/collections/PleIAs/toxic-commons-672243e8ce64b6759e79b6dc){:target="toxic-commons"} | 2024-11-04 |
| **Finance Commons** | A large collection of multimodal financial documents in open data | [Hugging Face](https://huggingface.co/collections/PleIAs/finance-commons-66925e1095c7fa6e6828e26c){:target="finance-commons"} | 2024-11-04 |
| **Bad Data Toolbox** | PleIAs collection of models for the data processing of challenging document and data sources | [Hugging Face](https://huggingface.co/collections/PleIAs/bad-data-toolbox-66981c2d0df662459252844e){:target="bad-data-toolbox"} | 2024-11-04 |
| **Open Culture** | A multilingual dataset of public domain books and newspapers | [Hugging Face](https://huggingface.co/collections/PleIAs/openculture-65d46e3ea3980fdcd66a5613){:target="open-culture"} | 2024-11-04 |
| **Math PDF** | A collection of open source PDFs on Mathematics | [Hugging Face](https://huggingface.co/datasets/PleIAs/Math-PDF){:target="math-pdf"} | 2025-03-19 |


## ServiceNow

Multimodal, code, and other datasets.

* ServiceNow [website](https://www.servicenow.com){:target="servicenow"}
* ServiceNow [Hugging Face organization](https://huggingface.co/ServiceNow){:target="servicenow-hf"}
* BigCode [Hugging Face organization](https://huggingface.co/bigcode){:target="big-code-hf"}

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **BigDocs-Bench** | A dataset for a comprehensive benchmark suite designed to evaluate downstream tasks that transform visual inputs into structured outputs, such as GUI2UserIntent (fine-grained reasoning) and Image2Flow (structured output). We are actively working on releasing additional components of BigDocs-Bench and will update this repository as they become available. | [Hugging Face](https://huggingface.co/datasets/ServiceNow/BigDocs-Bench){:target="bigdocs-bench"} | 2024-12-11 |
| **RepLiCA**   | RepLiQA is an evaluation dataset that contains Context-Question-Answer triplets, where contexts are non-factual but natural-looking documents about made up entities such as people or places that do not exist in reality... | [Hugging Face](https://huggingface.co/datasets/ServiceNow/repliqa){:target="replica"} | 2024-12-11 |
| **The Stack** | Exact deduplicated version of [The Stack](https://www.bigcode-project.org/docs/about/the-stack/){:target="the-stack"} dataset used for the [BigCode project](https://www.bigcode-project.org){:target="big-code"}. | [Hugging Face](https://huggingface.co/datasets/bigcode/the-stack){:target="the-stack-hf"} | 2024-12-11 |
| **The Stack Dedup** | Near deduplicated version of The Stack (recommended for training). | [Hugging Face](https://huggingface.co/datasets/bigcode/the-stack-dedup){:target="the-stack-dedup"} | 2024-12-11 |
| **StarCoder Data** | Pretraining dataset of [StarCoder](https://huggingface.co/blog/starcoder){:target="starcoder"}. | [Hugging Face](https://huggingface.co/datasets/bigcode/starcoderdata){:target="starcoderdata"} | 2024-12-11 |

## SemiKong

The training dataset for the [SemiKong](https://www.semikong.ai/){:target="semikong"} collaboration that trained an open model for the semiconductor industry.

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **SemiKong** | An open model training dataset for semiconductor technology | [Hugging Face](https://huggingface.co/datasets/pentagoniac/SemiKong_Training_Datset){:target="semikong-dataset"} | 2024-09-01 |

### `do-not-answer`

Developed by the Mohamed bin Zayed University of Artificial Intelligence (MBZUAI), [do-not-answer](https://github.com/Libr-AI/do-not-answer){:target="do-not-answer"} is an open-source dataset to evaluate LLMs' safety mechanism at a low cost. The dataset is curated and filtered to consist only of prompts to which responsible language models do not answer. Besides human annotations, Do not answer also implements model-based evaluation, where a 600M fine-tuned BERT-like evaluator achieves comparable results with human and GPT-4.

### Sony AI and the University of Tokyo

A collaboration of Sony AI and the University of Tokyo created the [Human-Centric Face Representations](https://ai.sony/publications/A-View-From-Somewhere-Human-Centric-Face-Representations/){:target="human-centric-faces"}, a collaboration to generate a dataset of 638,180 human judgments on face similarity. Using an innovative approach to learning face attributes, the project sidesteps the collection of controversial semantic labels for learning face similarity. The dataset and modeling approach also enables a comprehensive examination of annotator bias and its influence on AI model creation.

Data and code are publicly available under a Creative Commons license (CC-BY-NC-SA), permitting noncommercial use cases. See the [GitHub repo](https://github.com/SonyAI/a_view_from_somewhere){:target="human-centric-faces-github"}.

## Wikimedia Enterprise

Datasets from the Wikimedia Foundation, the organization that hosts and supports Wikipedia, Wikidata, and many other projects affiliated with the movement. 

* Wikimedia Enterprise [website](https://enterprise.wikimedia.com/){:target="wikimedia"}
* Wikimedia Enterprise [Hugging Face organization](https://huggingface.co/wikimedia){:target="wikimedia-hf"}.
* Wikimedia Enterprise [Collections on Hugging Face](https://huggingface.co/wikimedia/datasets){:target="wikimedia-hf-col"}
* Wikimedia Enterprise [Collections on Kaggle](https://www.kaggle.com/organizations/wikimedia-foundation/datasets){:target="wikimedia-kaggle-col"}
* Wikimedia Enterprise [GitHub Organization](https://github.com/wikimedia-enterprise){:target="github"}

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **Wikipedia Structured Contents** | Early beta release of the English and French Wikipedia articles including infoboxes| [Hugging Face](https://huggingface.co/datasets/wikimedia/structured-wikipedia){:target="structured-contents"} | 2024-09-16 |
| **Wikipedia Structured Contents** | Early beta release of the English and French Wikipedia articles including infoboxes | [Kaggle](https://www.kaggle.com/datasets/wikimedia-foundation/wikipedia-structured-contents){:target="structured-contents"} | 2024-09-16 |
| **Wikimedia Wikisource** | Wikisource dataset containing cleaned articles of all languages  |[Hugging Face](https://huggingface.co/datasets/wikimedia/wikisource){:target="wikisource"} | 2023-12-01 |
| **Wikimedia Wikipedia** | Wikipedia dataset containing cleaned articles of all languages | [Hugging Face](https://huggingface.co/datasets/wikimedia/wikipedia){:target="wikipedia"} | 2023-11-01 |
| **Wikimedia WIT** | WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning | [Hugging Face](https://huggingface.co/datasets/wikimedia/wit_base){:target="WIT"} [paper](https://arxiv.org/abs/2103.01913){:target="_blank"} | 2022-05-22 |

## Your Contributions?

To expand our catalog, [we welcome your contributions]({{site.baseurl}}/contributing).
