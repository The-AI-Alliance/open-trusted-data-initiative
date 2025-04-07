---
layout: default
title: Start Here!
nav_order: 10
has_children: true
---

# Open Trusted Data Initiative (OTDI) 
## Building the Future of Trustworthy Data for AI

{: .hightlight}
Join **The AI Alliance, Open Trusted Data Initiative** (OTDI), where our mission is to create a comprehensive, widely-sourced catalog of datasets with clear licenses for use, explicit provenance guarantees, and governed transformations, intended for AI model training, tuning, and application patterns like RAG (retrieval augmented generation) and agents.

In our context _trusted data_ means the provenance and governance of the dataset is clear and unambiguous. The metadata about the dataset provides clarity about its intended purposes, safety, and other considerations, along with any filtering and other processing steps that were done on the dataset.

OTDI is building a high-quality, trusted, and open catalog of datasets for AI LLM pre-training, fine-tuning, and domain-specific applications. These datasets are amenable to a wide variety of use cases in enterprises, governments, regulated industries, and wherever high trust in the data foundations of AI is essential.

Specifically, the initiative consists of **several projects that welcome your contributions:**

* [Define Openness Criteria]({{site.baseurl}}/dataset-requirements/): What has to be true about a dataset in order for it to be considered truly _open_ for use? This project defines those criteria. See the [list of open issues](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22dataset+requirements%22){:target="github"} for more details about our evolving thinking on the minimally-sufficient criteria.
* [Find Diverse Datasets]({{site.baseurl}}/contributing/#what-kinds-of-datasets-do-we-want): We seek a very broad range of datasets, including: text (especially under-served language), multimedia (audio, video, images), time series (targeting any domain or application), science (molecular discovery, drug discovery, geospatial, physics, etc., etc), specific domains and use cases (industry-specific and use case-specific data), synthetic (datasets for all of the above can be synthetic or "real"). See our [list of open issues](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22diverse+datasets%22){:target="github"} for a _partial_ list of desired datasets.
* [Data Pipelines]({{site.baseurl}}/our-processing/): Data pipelines implemented using tools like [DPK](https://github.com/The-AI-Alliance/dpk-alliance){:target="dpk"} are used both to validate datasets proposed for inclusion in our catalog and, eventually, to derive new datasets specialized for particular purposes. See the [list of open issues](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22data+pipelines%22){:target="github"} page for our current work.
* [Open Dataset Catalog]({{site.baseurl}}/catalog/): A catalog of datasets from many sources that meet our criteria for openness. See the [list of current issues](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22dataset+catalog%22){:target="github"} page for more information.

Please [join us]({{site.baseurl}}/about/#join-the-open-trusted-data-initiative)!

| See this short [presentation]({{site.baseurl}}/files/OTDI-Overview.pdf) (PDF) for more information about the Open Trusted Data Initiative. |

> **News:**
>
> * February 11, 2025: OTDI [announced](https://thealliance.ai/blog/announcing-open-trusted-data-initiative-otdi){:target="aias"} at the AI Action Summit in Paris. Added an [EPFL]({{site.baseurl}}/catalog/#epfl) dataset.
> * January 31, 2025: Added [Data for Good at Meta]({{site.baseurl}}/catalog/#meta) datasets.
> * January 23, 2025: The initiative [Steering Committee]({{site.baseurl}}/about/#steering-committee) is established.
> * December 11, 2024: Added [ServiceNow]({{site.baseurl}}/catalog/#servicenow) datasets.
> * November 20, 2024: [BrightQuery]({{site.baseurl}}/catalog/#brightquery) joins the AI Alliance and the Open Trusted Data Initiative: [LinkedIn announcement](https://www.linkedin.com/posts/jose-plehn_brightquery-is-proud-to-now-be-a-member-of-activity-7265516443742478338-xjIz/?utm_source=share&utm_medium=member_desktop){:target="bq-li"}.
> * November 4, 2024: [PleIAs]({{site.baseurl}}/catalog/#pleias) joins the AI Alliance and the Open Trusted Data Initiative: [LinkedIn announcement](https://www.linkedin.com/posts/pleias_pleias-joins-the-ai-alliance-to-co-lead-open-ugcPost-7259263514542796800-Uphx/){:target="pleias-li"}.
> * October 15, 2024: [Common Crawl Foundation]({{site.baseurl}}/catalog/#common-crawl-foundation) joins the AI Alliance and the Open Trusted Data Initiative.

> **Tip:** Use the search box at the top of this page to find specific content.

| **Authors**      | [The AI Alliance Open Trusted Data Work Group](https://thealliance.ai/focus-areas/foundation-models){:target="ai-alliance-wg"} |
| **Last Update**  | V0.2.7, 2025-03-18 |

## Why Is Trusted Data Important?

A significant challenge today for users of datasets is the desire for clear licenses to use the data, assurances that the data was sourced appropriately (the provenance), and trust that the data has been securely and traceably managed (governance).

OTDI aims to address these concerns with an industry wide effort to specify governance requirements and to catalog and process datasets fully in the open, allowing model developers and users to have full confidence in the provenance and governance of the data they use.

### Delivering Trust

What does delivering trust mean? We wish to enable the following:

* **Data Exploration:** Finding datasets that meet our governance specification and fully support your needs.
* **Data Cleaning:** Datasets processed for specific objectives (e.g., deduplication, hate speech removal, etc.) with open-source data pipelines.
* **Data Auditing:** End-to-end governance, ie., traceability, of all activity involving the dataset.
* **Data Documentation:** Metadata that covers all important aspects of a dataset.

Our deliverables to the industry will include the following:

* **Baseline Knowledge Datasets:** Openly accessible, permissively licensed language, code, image, audio, and video data that embodies a diverse range of global knowledge.
* **Domain Knowledge Datasets:** A rich, comprehensive set of datasets pertinent to tuning foundation models to a set of application domains: legal, finance, chemistry, manufacturing, etc.
* **Tooling and Platform Engineering:** Hosted pipelines, platform services, and compute capacity for synthetic dataset generation and data preparation at the scale needed to achieve the vision. Fully open-source, so you can use these tools as you see fit.

### The Value of Governance

Governance of datasets delivers these benefits:

* **Strengthens Trust:** Demonstrates a commitment to safeguarding data and enhancing its reputation.
* **Boosts Operational Efficiency:** Reduces redundancies and inefficiencies by ensuring consistent data management and quality practices.
* **Supports Innovation:** Having reliable, well-managed data can fuel analytics, AI, and other technological innovations.
* **Regulatory Compliance:** Helps organizations meet legal and industry-specific requirements (e.g., GDPR, HIPAA) by ensuring data is properly managed.
* **Facilitates Accountability:** Clarifies stewardship of data, ensuring responsibility for its integrity and usage.
* **Enhances Decision-Making:** Provides access to trusted, high-quality data, enabling better consumption and outcomes.

## Contributing Datasets

If you just want to browse the current catalog:<br/>
<a href="{{site.baseurl}}/catalog/" target="hugging-face" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph">click here</a>.

So, why should you get involved?

* **Collaborate on AI Innovation:** Your data can help build more accurate, fair, versatile, and open AI models. You can also connect with like-minded data scientists, AI researchers, and industry leaders in the AI Alliance.
* **Transparency & Trust:** Every contribution is transparent, with robust data provenance, governance, and trust mechanisms. We welcome your expertise to help us improve all aspects of these processes.
* **Tailored Contributions:** The world needs domain-specific datasets to enable model tuning to create open foundation models relevant to domains such as time series, and branches of science and industrial engineering. The world needs more multilingual, including underserved languages, and multimodel datasets. In many areas, the available real-world data is insufficient for the needs to innovate in those areas. Therefore, synthetic datasets are also needed.

### Next Steps

Interested in contributing a dataset to our catalog? Follow these steps:

1. Review our [Dataset Specification]({{site.baseurl}}/dataset-requirements), including creation of a [Hugging Face Dataset Card](https://huggingface.co/docs/hub/datasets-cards){:target="hf-card"}.
2. See [How We Process Datasets]({{site.baseurl}}/our-processing), i.e., the filtering and analysis steps we perform.
3. Finally, visit [Contribute Your Dataset]({{site.baseurl}}/contributing) and let us know about your dataset.

## More Information

* [References]({{site.baseurl}}/references): More details and other viewpoints on open, trusted data.
* [About Us]({{site.baseurl}}/about): More about the AI Alliance and this project.

### Version History

| Version  | Date       |
| :------- | :--------- |
| V0.2.7   | 2025-03-18 |
| V0.2.6   | 2025-02-11 |
| V0.2.5   | 2025-01-31 |
| V0.2.4   | 2025-01-21 |
| V0.2.3   | 2025-01-08 |
| V0.2.2   | 2024-12-11 |
| V0.2.1   | 2024-12-05 |
| V0.2.0   | 2024-12-04 |
| V0.1.0   | 2024-11-13 |
| V0.0.4   | 2024-11-04 |
| V0.0.3   | 2024-09-06 |
| V0.0.2   | 2024-09-06 |
| V0.0.1   | 2024-09-01 |
