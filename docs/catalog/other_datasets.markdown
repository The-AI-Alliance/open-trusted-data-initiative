---
layout: default
title: Other Datasets
nav_order: 500
has_children: false
parent: Dataset Catalog
---

# Other Datasets

Many other open datasets are not hosted at Hugging Face, so they are not yet part of our catalog. Other datasets that are hosted there aren't picked up by our metadata scans for various reasons. A common blocker is that some datasets are open access, but you have to request access explicitly before using them, even to get their Croissant metadata! This is an issue we will have to address.

For now, here is a list of notable datasets that don't appear in the catalog pages, grouped into general topic areas.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Benchmark and Other Evaluation Datasets

### NeurIPS 2024 Datasets Benchmarks

The NeurIPS 2024 [Datasets Benchmarks](https://neurips.cc/virtual/2024/events/datasets-benchmarks-2024){:target="neurips2024"} is a list of recently-created datasets of interest for evaluation.


## Chemistry

Many datasets for chemistry are open for use.

### CartBlanche

[CartBlanche](https://cartblanche.docking.org/){:target="_blank"} is an interface to ZINC-22, a free database of commercially-available compounds for virtual screening. From the website:

> ZINC-22 focuses on make-on-demand ("tangible") compounds from a small number of large catalogs: Enamine, WuXi and Mcule. Our sister database, [ZINC20](https://zinc20.docking.org/){:target="_blank"} focuses on smaller catalogs. ZINC-22 currently has about 54.9 billion molecules in 2D and 5.9 billion in 3D.

### PubChem

[PubChem](https://pubchem.ncbi.nlm.nih.gov/docs/downloads){:target="_blank"} is a free-to-use chemistry database. From the website:

> PubChem is a free to use database with most of the data readily available for download. Exceptions may exist in cases where licensing agreements prevent our data contributors from allowing bulk downloads of some data sets.
>
> Please consult the NCBI Policies and Disclaimers webpage (https://www.ncbi.nlm.nih.gov/home/about/policies/){:target="_blank"} and the NLM Web Policies webpage (https://www.nlm.nih.gov/web_policies.html){:target="_blank"}.
>
> The data in PubChem comes from hundreds of data contributors (https://pubchem.ncbi.nlm.nih.gov/source/){:target="_blank"}. A data source may provide explicit data license information. One should check with the PubChem data source for the most current data licensing information.
>
> PubChem strives to make clear the data provenance of all content. Within a given data table row or beneath provided content, the data provenance is provided. For example, this data shows Medical Subject Headings (MeSH) as the data source for the assertion of a chemical being a “Fibrinolytic Agent”:

## Text

### Institutional Data Initiative

The [Institutional Data Initiative] at the Harvard Law School Library has published [The Institutional Books Corpus](https://www.institutionaldatainitiative.org/institutional-books). This dataset is [available on Hugging Face](https://huggingface.co/datasets/institutional/institutional-books-1.0), but it is not in our catalog, because currently access to it, even its Croissant metadata, requires prior approval.

## Other Datasets?

If you know of other open datasets that we should include in our catalog, [let us know]({{site.baseurl}}/contributing).
