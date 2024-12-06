---
layout: default
title: Start Here!
nav_order: 10
has_children: true
---

# Building the Future of Open, Trusted Data for AI

{: .hightlight}
> _Join **The AI Alliance, Open Trusted Data Initiative** (OTDI), where our mission is to create a comprehensive, widely-sourced catalog of datasets with clear licenses for use, explicit provenance guarantees, and governed transformations, intended for AI model training, tuning, and application patterns like RAG (retrieval augmented generation) and agents._
>
> _In our context_ trusted data _means the provenance and governance of the dataset is clear and unambiguous. The metadata about the dataset provides clarity about its intended purposes, safety, and other considerations, along with any filtering and other processing steps that were done on the dataset._

> **News:**
>
> * November 20, 2024: [BrightQuery](https://brightquery.com/){:target="bq"} joins the AI Alliance and the Open Trusted Data Initiative: [LinkedIn announcement](https://www.linkedin.com/posts/jose-plehn_brightquery-is-proud-to-now-be-a-member-of-activity-7265516443742478338-xjIz/?utm_source=share&utm_medium=member_desktop){:target="bq-li"}.
> * November 4, 2024: [pleias](https://pleias.fr){:target="pleias"} joins the AI Alliance and the Open Trusted Data Initiative: [LinkedIn announcement](https://www.linkedin.com/posts/pleias_pleias-joins-the-ai-alliance-to-co-lead-open-ugcPost-7259263514542796800-Uphx/){:target="pleias-li"}.
> * October 15, 2024: [Common Crawl Foundation](https://commoncrawl.org/){:target="ccf"} joins the AI Alliance and the Open Trusted Data Initiative.

> **Tip:** Use the search box at the top of this page to find specific content.

| **Authors**     | [The AI Alliance Open Trusted Data Work Group](https://thealliance.ai/focus-areas/foundation-models){:target="ai-alliance-wg"} |
| **Last Update** | V0.1.0, 2024-11-13 |

# Why Is Trusted Data Important?

A significant challenge today is the &ldquo;murky&rdquo; provenance of many datasets used for training foundation models (FMs), like large language models (LLMs). Model developers and users risk the potential for models regenerating private, confidential, and copyrighted information that might have been part of the training dataset, among other concerns. This is one of the reasons that most models that allow unrestricted (&ldquo;open&rdquo;) use rarely include publication of their training dataset and the full source code for all the filtering and transformation steps used to create that dataset, from initial acquisition to its final form before training. At best, _open models_ limit themselves to descriptions in general terms of the data sources and methods used.

OTDI aims to address these concerns with an industry wide effort to gather and process data fully in the open, allowing model developers and users to have full confidence in the provenance and governance of the data they use.

## Delivering Trust

What does delivering trust mean? We wish to enable the following:

* **Data Exploration:** Finding datasets that meet your governance specification and fully support your needs.
* **Data Cleaning:** Datasets processed for specific objectives (e.g., deduplication, hate speech removal, etc.) with open-source data pipelines.
* **Data Auditing:** End-to-end governance, ie., traceability, of all activity involving the dataset.
* **Data Documentation:** Metadata that covers all important aspects of a dataset.

Our deliverables to the industry will include the following:

* **Baseline Knowledge Datasets:** Openly accessible, permissively licensed language, code, image, audio, and video data that embodies a diverse range of global knowledge. 
* **Domain Knowledge Datasets:** A rich, comprehensive set of datasets pertinent to tuning foundation models to a set of application domains: legal, finance, chemistry, manufacturing, etc.
* **Tooling and Platform Engineering:** Hosted pipelines, platform services, and compute capacity for synthetic dataset generation and data preparation at the scale needed to achieve the vision. Fully open-source, so you can use these tools as you see fit.

# Contributing Datasets

If you just want to browse the current catalog:<br/>
<a href="{{site.baseurl}}/catalog/" target="hugging-face" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph">click here</a>.

So, why should you get involved?

* **Collaborate on AI Innovation:** Your data can help build more accurate, fair, versatile, and open AI models. You can also connect with like-minded data scientists, AI researchers, and industry leaders in the AI Alliance.
* **Transparency & Trust:** Every contribution is transparent, with robust data provenance, governance, and trust mechanisms. We welcome your expertise to help us improve all aspects of these processes.
* **Tailored Contributions:** The world needs domain-specific datasets to enable model tuning to create open foundation models relevant to domains such as time series, and branches of science and industrial engineering. The world needs more multilingual, including underserved languages, and multimodel datasets. In many areas, the available real-world data is insufficient for the needs to innovate in those areas. Therefore, synthetic datasets are also needed.

## Next Steps

Interested in contributing a dataset to our catalog? Follow these steps:

1. Review our [Dataset Specification]({{site.baseurl}}/dataset-specification), including creation of a [Hugging Face Dataset Card](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"}.
2. See [How We Process Datasets]({{site.baseurl}}/our-processing), i.e., the filtering and analysis steps we perform.
3. Finally, visit [Contribute Your Dataset]({{site.baseurl}}/contributing) and let us know about your dataset.

## More Information

* [References]({{site.baseurl}}/references): More details and other viewpoints on open, trusted data.
* [About Us]({{site.baseurl}}/about): More about the AI Alliance and this project.

### Version History

| **Versions** | **Dates**  |
| V0.1.0       | 2024-11-13 |
| V0.0.4       | 2024-11-04 |
| V0.0.3       | 2024-09-06 |
| V0.0.2       | 2024-09-06 |
| V0.0.1       | 2024-09-01 |
