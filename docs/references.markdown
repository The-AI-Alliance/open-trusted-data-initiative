---
layout: default
title: References
nav_order: 60
has_children: false
---

# References: Other Information About Trusted, Open Data

Here is an evolving list of writings from other sources about the importance of open, trusted data, implications, technologies used, etc. Of course, the opinions expressed do not necessarily reflect the views of the AI Alliance. However, many of these sources influence our work.

> **Help Wanted:** If you have other references you like, please let us know through email, [data@thealliance.ai](mailto:data@thealliance.ai), or [edit this page](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/latest/docs/references.markdown){:target='repo'}!

This section is organized by topic.

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

> The purpose of the paper we are sharing today is twofold. It clarifies the categories of rights and legitimate interests that justify access to information about training data. In addition to copyright, these include, among others, privacy and personal data protection, scientific freedom, the prohibition of discrimination, and respect for cultural and linguistic diversity. Moreover, it provides a blueprint for the forthcoming template for the &ldquo;sufficiently detailed summary,&rdquo; which is intended to serve these interests while respecting the rights of all parties concerned.

## Licensing and Attribution

### A Large-scale Audit of Dataset Licensing and Attribution in AI

[A large-scale audit of dataset licensing and attribution in AI](https://www.nature.com/articles/s42256-024-00878-8){:target="nature"} is a Nature paper from MIT researchers and others. From a corresponding [MIT News article](https://news.mit.edu/2024/study-large-language-models-datasets-lack-transparency-0830){:target="mit"}, the paper describes their "... systematic audit of more than 1,800 text datasets on popular hosting sites. They found that more than 70 percent of these datasets omitted some licensing information, while about 50 percent had information that contained errors.

"Building off these insights, they developed a user-friendly tool called the Data Provenance Explorer that automatically generates easy-to-read summaries of a dataset’s creators, sources, licenses, and allowable uses."

## Data Provenance and Governance

### Data Provenance Initiative

[Website](https://www.dataprovenance.org/){:target="dp-site"}, [GitHub](https://github.com/Data-Provenance-Initiative/Data-Provenance-Collection){:target="dp-repo"}

There mission is to uncover the datasets used to train large language models. From their website:

> The Data Provenance Initiative is a volunteer collective of AI researchers from around the world. We conduct large-scale audits of the massive datasets that power state-of-the-art AI models. We have audited over 4,000 popular text, speech, and video datasets, tracing them from origin to creation, cataloging data sources, licenses, creators, and other metadata, which researchers can examine using our Explorer tool. We recently analyzed 14,000 web domains, to understand the evolving provenance and consent signals behind AI data. The purpose of this work is to map the landscape of AI data, improving transparency, documentation, and informed use of data.

### Data and Trust Alliance - Data Provenance Standards

The [Data and Trust Alliance](https://dataandtrustalliance.org/){:target="dta"} has defined a standard for [provenance](https://dataandtrustalliance.org/work/data-provenance-standards){:target="dta-prov"}, as well as other projects.

Here is their statement about the purpose of this standard, quoted from the project web page:

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

<a name="ai-bom"></a>
## Bill of Materials

### The Linux Foundation - Implementing AI Bill of Materials (AI BOM) with SPDX 3.0

A _bill of materials_ is a traditional concept used to specify for producers and consumers exactly what parts are contained in the whole. They have been used in shipping for a very long time, for example.

Software BoMs have the same goals, to very clearly state what components a software artifact contains.

[This Linux Foundation report](https://www.linuxfoundation.org/research/ai-bom){:target="ai-bom"} discusses the concept in the content of AI. A quote from the website:

> A Software Bill of Materials (SBOM) is becoming an increasingly important tool in regulatory and technical spaces to introduce more transparency and security into a project's software supply chain.
> 
> Artificial intelligence (AI) projects face unique challenges beyond the security of their software, and thus require a more expansive approach to a bill of materials. In this report, we introduce the concept of an AI-BOM, expanding on the SBOM to include the documentation of algorithms, data collection methods, frameworks and libraries, licensing information, and standard compliance.
