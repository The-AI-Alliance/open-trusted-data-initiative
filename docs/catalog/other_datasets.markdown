---
layout: default
title: Other Datasets
nav_order: 500
has_children: false
parent: Dataset Catalog
---

# Other Datasets

Many open datasets are not hosted at Hugging Face, so they are not yet part of our catalog. Other datasets that are hosted there aren't picked up by our catalog building process for various reasons, some of which are discussed in [About This Catalog]({{site.baseurl}}/catalog/catalog/). For example, Croissant metadata might not be available, licenses may be incorrectly defined or missing, or it may be required to manually request access to a dataset, even before you can see its Croissant metadata!

For now, here is a list of notable datasets that don't appear in the catalog pages, grouped into general topic areas. See also the [Contributors]({{site.baseurl}}/catalog/contributors/) page.

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
> Please consult the NCBI [Policies and Disclaimers](https://www.ncbi.nlm.nih.gov/home/about/policies/){:target="_blank"} webpage and the [NLM Web Policies](https://www.nlm.nih.gov/web_policies.html){:target="_blank"} webpage.
>
> The data in PubChem comes from hundreds of data [contributors](https://pubchem.ncbi.nlm.nih.gov/source/){:target="_blank"}. A data source may provide explicit data license information. One should check with the PubChem data source for the most current data licensing information.
>
> PubChem strives to make clear the data provenance of all content. Within a given data table row or beneath provided content, the data provenance is provided. For example, this data shows Medical Subject Headings (MeSH) as the data source for the assertion of a chemical being a “Fibrinolytic Agent”:

## Text

### Common Pile

Another large open dataset, _Common Pile_ ([HF announcement](https://huggingface.co/blog/common-pile/common-pile-v0p1-announcement){:target="_blank"}, [HF location](https://huggingface.co/common-pile){:target="_blank"}, [HF blog](https://huggingface.co/blog/stellaathena/common-pile){:target="_blank"}, [Paper](https://github.com/r-three/common-pile/blob/main/paper.pdf){:target="_blank"}, [Code](https://github.com/r-three/common-pile){:target="_blank"}), was published in June 2025 by a consortium of researchers from University of Toronto, Vector Institute, Hugging Face, EleutherAI, The Allen Institute for Artificial Intelligence, Teraflop AI, Cornell University, University of Maryland College Park, MIT, CMU, Lila Sciences, Lawrence Livermore National Laboratory, etc. See also the PleIAs' [Common Corpus]({{site.baseurl}}/catalog/contributors/#pleias) dataset.

The Common Pile collaborators used 1 trillion and 2 trillion token subsets of Common Pile as [training datasets](https://huggingface.co/datasets/common-pile/comma_v0.1_training_dataset){:target="_blank"} for two models, [Comma-v0.1-1t](https://huggingface.co/common-pile/comma-v0.1-1t){:target="_blank"} and [Comma-v0.1-2t](https://huggingface.co/common-pile/comma-v0.1-2t){:target="_blank"}, respectively. Both are 7B parameter models.

> **NOTE:** Because this dataset is published in Hugging Face, it will appear in our catalog soon.

### Institutional Data Initiative

The [Institutional Data Initiative] at the Harvard Law School Library has published [The Institutional Books Corpus](https://www.institutionaldatainitiative.org/institutional-books){:target="_blank"}. This dataset is [available on Hugging Face](https://huggingface.co/datasets/institutional/institutional-books-1.0){:target="_blank"}, but it is not in our catalog, because currently access to it, even its Croissant metadata, requires prior approval.

## Other Datasets?

If you know of other open datasets that we should include in our catalog, [let us know]({{site.baseurl}}/contributing).
