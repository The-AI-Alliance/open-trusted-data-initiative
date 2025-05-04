---
layout: default
title: Start Here!
nav_order: 10
has_children: false
language_tags: English, Molecular
---

# Open Trusted Data Initiative (OTDI) 

## Take Me to the Data!

### Languages

<div class="table-wrapper">
  {% for language in site.language %}
  <a href="{{site.baseurl}}/catalog/#{{language.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{language.name}}</a>
  {% endfor %}
</div>

### Domains

<div class="table-wrapper">
  {% for domain in site.domain %}
  <a href="{{site.baseurl}}/catalog/#{{domain.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{domain.name}}</a>
  {% endfor %}
</div>

### Modalities

<div class="table-wrapper">
  {% for modality in site.modality %}
  <a href="{{site.baseurl}}/catalog/#{{modality.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{modality.name}}</a>
  {% endfor %}
</div>


## Help Us Build the Future of Trustworthy Data for AI

{: .hightlight}
The mission of **Open Trusted Data Initiative** (OTDI) is to create a comprehensive, widely-sourced **catalog of datasets** with **clear licenses for use**, **explicit provenance guarantees**, and **governed lifecycles**. These datasets are suitable for AI model training, tuning, and application patterns like RAG (retrieval augmented generation) and agents.

### What Does _Trusted Data_ Mean?

Is the provenance and governance of a dataset clear and unambiguous? Does the metadata about the dataset provide clarity about its intended purposes, safety, and other considerations? What sources and processing were used to create the dataset?

Creating a catalog of trusted data involves several projects. **We welcome your contributions:**

#### Define the Criteria for Open and Trustworthy Data

Our definition of these [criteria]({{site.baseurl}}/dataset-requirements/) is evolving. Help us [refine them](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22dataset+requirements%22){:target="github"}.

#### Find and Catalog Datasets for Diverse Topics

AI models and applications need datasets covering a broad [range of topics]({{site.baseurl}}/contributing/#what-kinds-of-datasets-do-we-want) including: 

* **Text:** Especially for under-served language
* **Multimedia:** Images, video, audio
* **Time series:** General purpose and domain-specific
* **Science and Technology:** Materials, drug discovery, geospatial, physics, etc.
* **Specific domains and use cases:** Healthcare, legal, financial, education, chat bots, etc.
* **Synthetic datasets:** For all of the above categories, synthetic datasets are needed, too.

What datasets [can you add to our catalog?](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22diverse+datasets%22){:target="github"}.

#### Build Data Processing Pipelines

[Data Pipelines]({{site.baseurl}}/our-processing/) are used to validate datasets proposed for inclusion in our catalog and to derive new datasets specialized for particular purposes. Are you a data processing expert? [We need your help](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22data+pipelines%22){:target="github"}.

#### Build a Searchable Dataset Catalog

Currently, the [Dataset Catalog]({{site.baseurl}}/catalog/) is a static resource. Help us make it [browsable and searchable](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22dataset+catalog%22){:target="github"}.


| See this short [presentation]({{site.baseurl}}/files/OTDI-Overview.pdf) (PDF) for more information about the Open Trusted Data Initiative. |

# More Information

* What [trustworthiness]({{site.baseurl}}/trustworthiness) means to us.
* [About Us]({{site.baseurl}}/about): More about the AI Alliance and this project.
* [References]({{site.baseurl}}/references): Other viewpoints on open, trusted data.
