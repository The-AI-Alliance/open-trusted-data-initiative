---
layout: default
title: Dataset Catalog
nav_order: 20
has_children: true
---

# The Dataset Catalog

{% comment %}
<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>
{% endcomment %}

{: .attention}
> **About This Catalog**
>
> We learned a **lot** about the quality of datasets by examining the metadata for the datasets hosted by Hugging Face. The tables in this catalog list the metadata for a small subset of these datasets, _small_ because of how we had to filter them. Here are the details of that process:
>
> * The tables reflect a snapshot of the datasets as of July 20<sup>th</sup>, 2025. We will update the snapshot approximately monthly while we work on a more automated, incremental, and iterative process.
> * The numbers discussed next reflect the snapshot processing from a previous run on June 5<sup>th</sup>, 2025. The _characteristics_ we describe don't change, while all the numbers gradually increase as more datasets are added to Hugging Face every day. We also round the numbers to the nearest thousands ("Ks").
> * Of the approximately 413K Hugging Face datasets (as of June 5<sup>th</sup>), 329K of them have queryable [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata. Among the remaining 84K, 66K don't have Croissant metadata and 18K _may_ have this metadata, but you are required to request permission to use the dataset first, even to query its metadata!
> * Of the remaining 329K datasets, 252K do **not** specify a license of any kind, so we discard them, leaving just 77K!
> * Of the remaining 77K datasets, 17K "attempt" to define licenses, but do so improperly. Licenses are specified as [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, 17.6K datasets specify undefined (i.e., &ldquo;404&rdquo;) URLs. We discard those datasets, leaving 59.4K.<a href="#footnote1"><sup>1</sup></a>
>
> How we group the remaining 59.4K datasets into tables using the `keywords` in the metadata:
>
> * The groupings are based on the presence of relevant `keywords`. The metadata for the datasets all have a `language` field, but **all** contain _either `en` (English) or `NULL`, so we ignore this field. However, many datasets have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)!).
> * All keywords were converted to lower case before grouping.
> * When a section for a keyword lists _additional keywords_, it means we grouped together different keywords that we believe are related to the same topic, including synonyms. (Please [email us about any errors](mailto:data@thealliance.ai?subject=Errors in the OTDI catalog) or report problems [another way]({{site.baseurl}}/contributing)) In these cases, we also show a **Keyword** column in the corresponding table, so you can see which keyword was used to include the dataset. (This also means that occasionally some datasets will be listed more than once in their table.)
>
> **Important:** At this time, we are not yet validating datasets to ensure their metadata accurately reflect the data records themselves.
>
> **Note:** Some of the datasets filtered out for one of the reasons discussed above are listed separately in our [Contributors]({{site.baseurl}}/catalog/contributors) or [Other Datasets]({{site.baseurl}}/catalog/other_datasets) pages, where we also describe some other useful datasets that are not available in Hugging Face and not yet included in the catalog itself.
>
> <a name="#footnote1">1</a>: Some of the bad license links clearly intend to reference known licenses. We will revisit those cases.
>
> Do you know of any datasets that should be shown, but aren't? Let us know through [email](mailto:data@thealliance.ai?subject=A dataset for the OTDI catalog) or [another way]({{site.baseurl}}/contributing).

# The Current Keywords Cataloged

## [Datasets For Languages]({{site.baseurl}}/catalog/language/language)

<div>
{% comment %} We loop over site.language repeatedly. Is there a more efficient approach? {% endcomment %}
{% assign current_region = "" %}
{% for member in site.language %}
  {% if member.tag == "language" %}
    {{ member.content }}
    {% assign subcategories = member.subcategories | split: '|' %}
    {% for sub in subcategories %}
      {% for member2 in site.language %}
        {% if member2.tag == sub %}
          <h3><a href="{{site.baseurl}}/catalog/language/{{member2.tag}}/">{{member2.name}}</a></h3>
          {{ member2.content }}
        {% endif %}
      {% endfor %}
    {% endfor %}
  {% endif %}
{% endfor %}
</div>

## [Datasets For Domains]({{site.baseurl}}/catalog/domain/)

<div>
{% for member in site.domain %}
  {% if member.tag == "domain" %}
    {{member.content}}
  {% endif %}
{% endfor %}
</div>

## [Datasets For Modalities]({{site.baseurl}}/catalog/modality/)

<div>
{% for member in site.modality %}
  {% if member.tag == "modality" %}
    {{member.content}}
  {% endif %}
{% endfor %}
</div>
