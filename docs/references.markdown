---
layout: default
title: References
nav_order: 70
has_children: false
---

# References: Other Information About Trusted, Open Data

Here is an evolving list of writings from other sources about the importance of open, trusted data, implications, technologies used, etc. Of course, the opinions expressed do not necessarily reflect the views of the AI Alliance. However, many of these sources influence our work.

{: .attention}
> **Help Wanted:** If you have other references you like, please let us know through email, [data@thealliance.ai](mailto:data@thealliance.ai?subject=A suggestion for the OTDI project), or [edit this page](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/main/docs/references.markdown){:target='repo'}!

This section is organized by topic.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Research Progress on Gathering and Using Open Datasets

While there are many open datasets of various sizes and areas of focus, a few attempts have been made to create very broad, completely open datasets suitable for training competitive foundation models.

### Pleias

In December 2024, [Pleias](https://pleias.fr){:target="_blank"} published [Common Corpus](https://huggingface.co/collections/PleIAs/common-corpus-6734e0f67ac3f35e44075f93){:target="common-corpus"}, a two trillion token dataset, and used it to train [several models](https://huggingface.co/PleIAs){:target="_blank"}. ([paper](https://arxiv.org/abs/2506.01732){:target="_blank"})

The Pleias datasets are discussed in more detail on the [contributors]({{site.baseurl}}/catalog/contributors/#pleias) page.

### Common Pile

Another large open dataset, _Common Pile_ ([HF announcement](https://huggingface.co/blog/common-pile/common-pile-v0p1-announcement){:target="_blank"}, [HF location](https://huggingface.co/common-pile){:target="_blank"}, [HF blog](https://huggingface.co/blog/stellaathena/common-pile){:target="_blank"}, [Paper](https://github.com/r-three/common-pile/blob/main/paper.pdf){:target="_blank"}, [Code](https://github.com/r-three/common-pile){:target="_blank"}), was published in June 2025 by a consortium of researchers from University of Toronto, Vector Institute, Hugging Face, EleutherAI, The Allen Institute for Artificial Intelligence, Teraflop AI, Cornell University, University of Maryland College Park, MIT, CMU, Lila Sciences, Lawrence Livermore National Laboratory, etc.

They used 1 trillion and 2 trillion token subsets of Common Pile as [training datasets](https://huggingface.co/datasets/common-pile/comma_v0.1_training_dataset){:target="_blank"} for two models, [Comma-v0.1-1t](https://huggingface.co/common-pile/comma-v0.1-1t){:target="_blank"} and [Comma-v0.1-2t](https://huggingface.co/common-pile/comma-v0.1-2t){:target="_blank"}, respectively. Both are 7B parameter models.

{: .note}
> **NOTE:** Because this dataset is published in Hugging Face, it will appear in our "snapshot" static catalog soon.

## Avoiding &ldquo;AI Slop&rdquo;

The blog [Low-background Steel (Pre AI)](https://lowbackgroundsteel.ai){:target="_blank"} catalogs datasets known to predate the announcement of ChatGPT, after which AI-generated content became more and more prevalent in datasets. This site wants to ensure that _pure_, human-generated datasets exist for research and development. From the site:

{: .attention}
> Sources of data that haven’t been contaminated by AI-created content. Low-background Steel (and lead) is a type of metal uncontaminated by radioactive isotopes from nuclear testing. That steel and lead is usually recovered from ships that sunk before the Trinity Test in 1945. This blog is about uncontaminated content that I'm terming "Low-background Steel". The idea is to point to sources of text, images and video that were created prior to the explosion of AI-generated content that occurred in 2022.

## General Data Concerns

<a name="data-transparency"></a>
### Hugging Face: Training Data Transparency in AI: Tools, Trends, and Policy Recommendations

[Blog post](https://huggingface.co/blog/yjernite/data-transparency){:target="hf-data-transparency"} by [Yacine Jernite](https://huggingface.co/yjernite){:target="yacine"}.

A call for &ldquo;minimum meaningful public transparency standards to support effective AI regulation.&rdquo;

### U.S. Department of Commerce

[Generative Artificial Intelligence and Open Data: Guidelines and Best Practices](https://www.commerce.gov/news/blog/2025/01/generative-artificial-intelligence-and-open-data-guidelines-and-best-practices){:target="usdc-pdf"}) ([PDF](https://www.commerce.gov/sites/default/files/2025-01/GenerativeAI-Open-Data.pdf){:target="usdc-pdf"}). This guidance is intended to be used by the department and its bureaus, but it is generally useful.

Note that it was published January 16, 2025, just before the end of the Biden administration. It is not clear if these guidelines will be retained by the new administration.

### The European Union AI Act - Data Implications

The [The European AI Office](https://digital-strategy.ec.europa.eu/en/policies/ai-office){:target="ai-office"} of the European Union has responsibility for implementing the [AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai){:target="ai-act"}, which &ldquo;... is the first-ever legal framework on AI, which addresses the risks of AI and positions Europe to play a leading role globally.&rdquo;

[Open Future](https://openfuture.eu/){:target="open-future"}, in collaboration with the [Mozilla Foundation](https://foundation.mozilla.org/en/?gad_source=1){:target="mozilla"}, has authored a [white paper](https://openfuture.eu/publication/towards-robust-training-data-transparency/){:target="open-future-paper"} called _Suffiently Detailed? A proposal for implementing the AI Act’s training data transparency specification for GPAI_ (general-purpose AI). This paper discusses new specification for model developers to produce a _sufficiently detailed summary_ of the content used for model training. [The announcement](https://openfuture.eu/publication/towards-robust-training-data-transparency/){:target="open-future-paper"} says the following:

{: .attention}
> The purpose of the paper we are sharing today is twofold. It clarifies the categories of rights and legitimate interests that justify access to information about training data. In addition to copyright, these include, among others, privacy and personal data protection, scientific freedom, the prohibition of discrimination, and respect for cultural and linguistic diversity. Moreover, it provides a blueprint for the forthcoming template for the &ldquo;sufficiently detailed summary,&rdquo; which is intended to serve these interests while respecting the rights of all parties concerned.

### Five Star Open Data

[Five Star Open Data](https://5stardata.info/en/){:target="5sd"} is a concept promoted by Tim Berners-Lee, the inventor of the Web and Linked Data initiator, which suggests a 5-star deployment scheme for Open Data:

| Stars | Description | 
| :===: | :========== | 
|   ★   | &ldquo;Make your stuff available on the Web (whatever format) under an open license.&rdquo; | 
|   ★★  | &ldquo;Make it available as structured data (e.g., Excel instead of image scan of a table).&rdquo; |
|  ★★★  | &ldquo;Make it available in a non-proprietary open format (e.g., CSV instead of Excel).&rdquo; |
|  ★★★★ | &ldquo;Use URIs to denote things, so that people can point at your stuff.&rdquo; |
| ★★★★★ | &ldquo;Link your data to other data to provide context.&rdquo; |

The website gives examples for each step of the stars and explains costs and benefits that come along with it.

## FAIR Principles

[Website](https://www.go-fair.org/fair-principles/){:target="fair"}

Quoting from the website:

{: .attention}
> In 2016, the [FAIR Guiding Principles for scientific data management and stewardship](https://www.nature.com/articles/sdata201618){:target="fair2"} were published in _Scientific Data_. The authors intended to provide guidelines to improve the Findability, Accessibility, Interoperability, and Reuse of digital assets. The principles emphasize machine-actionability (i.e., the capacity of computational systems to find, access, interoperate, and reuse data with none or minimal human intervention) because humans increasingly rely on computational support to deal with data as a result of the increase in volume, complexity, and creation speed of data.

Both data and metadata must be ***findable*** to be usable, such as storage in known locations. Machine readability is essential for practical use.

Data must be ***accessible*** through established tools (e.g., web APIs), possibly including authentication and authorization.

Datasets often need to be combined, requiring ***interoperable*** tools, storage, etc.

Ultimately, the goal is to make data ***reusable***, leading to requirements for clear licensing, provenance, and governance.

Finally, they define three **types of entities**: "data (or any digital object), metadata (information about that digital object), and infrastructure." For instance, findable means that both metadata and data are registered or indexed in a searchable resource (an infrastructure component).

## Licensing and Attribution

### A Large-scale Audit of Dataset Licensing and Attribution in AI

[A large-scale audit of dataset licensing and attribution in AI](https://www.nature.com/articles/s42256-024-00878-8){:target="nature"} is a Nature paper from MIT researchers and others. From a corresponding [MIT News article](https://news.mit.edu/2024/study-large-language-models-datasets-lack-transparency-0830){:target="mit"}, the paper describes their "... systematic audit of more than 1,800 text datasets on popular hosting sites. They found that more than 70 percent of these datasets omitted some licensing information, while about 50 percent had information that contained errors.

"Building off these insights, they developed a user-friendly tool called the Data Provenance Explorer that automatically generates easy-to-read summaries of a dataset’s creators, sources, licenses, and allowable uses."

## Data Provenance and Governance

### Data Provenance Initiative

[Website](https://www.dataprovenance.org/){:target="dp-site"}, [GitHub](https://github.com/Data-Provenance-Initiative/Data-Provenance-Collection){:target="dp-repo"}

There mission is to uncover the datasets used to train large language models. From their website:

{: .attention}
> The Data Provenance Initiative is a volunteer collective of AI researchers from around the world. We conduct large-scale audits of the massive datasets that power state-of-the-art AI models. We have audited over 4,000 popular text, speech, and video datasets, tracing them from origin to creation, cataloging data sources, licenses, creators, and other metadata, which researchers can examine using our Explorer tool. We recently analyzed 14,000 web domains, to understand the evolving provenance and consent signals behind AI data. The purpose of this work is to map the landscape of AI data, improving transparency, documentation, and informed use of data.

### Data and Trust Alliance - Data Provenance Standards

The [Data and Trust Alliance](https://dataandtrustalliance.org/){:target="dta"} has defined a standard for [provenance](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"}, as well as other projects.

Here is their statement about the purpose of this standard, quoted from the project web page:

{: .attention}
> For AI to create value for business and society, the data that trains and feeds models must be trustworthy.
>
> Trust in data starts with transparency into provenance; assessing where data comes from, how it’s created, and whether it can be used, legally. Yet the ecosystem needs a common language to provide that transparency.
>
> This is why we developed the first cross-industry data provenance standards.

## Data Classification

### Interactive Advertising Bureau Taxonomy

[Interactive Advertising Bureau](http://www.iabtechlab.com/){:target="iab"} ([GitHub](https://github.com/InteractiveAdvertisingBureau){:target="iab-gh"}) has defined a [taxonomy](https://iabtechlab.com/standards/content-taxonomy/){:target="iab-tax"} ([GitHub](https://github.com/InteractiveAdvertisingBureau/Taxonomies){:target="iab-tax-gh"}) of _content_, _audience_, and _ad products_ ([latest - V3.1](https://github.com/InteractiveAdvertisingBureau/Taxonomies/blob/develop/Content%20Taxonomies/Content%20Taxonomy%203.1.tsv){:target="iab-tax-31"}).

### IBM watsonx Natural Language Processing Categories

IBM's [watsonx](https://www.ibm.com/docs/en/watsonx/saas){:target="watson-nlp"}  Natural Language Processing (NLP) system works with a defined taxonomy of [categories](https://www.ibm.com/docs/en/watsonx/saas?topic=categorization-category-types){:target="watson-nlp-categories"}.

## Searching for Datasets

### University of California Berkeley

[It Took Longer than I was Expecting: Why is Dataset Search Still so Hard?](https://dl.acm.org/doi/10.1145/3665939.3665959){:target="hard"} analyzes why searching for datasets is harder than it might seem.

<a name="ai-bom"></a>
## Bill of Materials

### The Linux Foundation - Implementing AI Bill of Materials (AI BOM) with SPDX 3.0

A _bill of materials_ is a traditional concept used to specify for producers and consumers exactly what parts are contained in the whole. They have been used in shipping for a very long time, for example.

Software BoMs have the same goals, to very clearly state what components a software artifact contains.

[This Linux Foundation report](https://www.linuxfoundation.org/research/ai-bom){:target="ai-bom"} discusses the concept in the content of AI. A quote from the website:

{: .attention}
> A Software Bill of Materials (SBOM) is becoming an increasingly important tool in regulatory and technical spaces to introduce more transparency and security into a project's software supply chain.
>
> Artificial intelligence (AI) projects face unique challenges beyond the security of their software, and thus require a more expansive approach to a bill of materials. In this report, we introduce the concept of an AI-BOM, expanding on the SBOM to include the documentation of algorithms, data collection methods, frameworks and libraries, licensing information, and standard compliance.
