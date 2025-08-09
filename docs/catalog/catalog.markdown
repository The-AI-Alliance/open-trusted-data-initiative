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

{: .highlight}
> **About This Catalog**
>
> The tables in this catalog list the metadata for Hugging Face-hosted datasets that were gathered as follows:
>
> * The tables reflect a snapshot of the datasets as of July 20<sup>th</sup>, 2025. (We will do this approximately monthly while we work on a more &ldquo;dynamic&rdquo; process.)
> * The numbers discussed next reflect the snapshot processing from a previous run on June 5<sup>th</sup>, 2025. (More datasets are added to Hugging Face every day...)
> * Of the approximately 413,000 Hugging Face datasets, 329,000 of them have queryable [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata.
> * Of the 329,000  with Croissant data, we discard datasets with no license specified, leaving just 84,000!
> * Among the remaining 84,000, 66,000 don't have available Croissant data and 18,000 require you to request permission to use them first, even to query their Croissant metadata. Hence, these 84,000 datasets are not in our catalog tables. However, some of them are listed separately in our [Contributors]({{site.baseurl}}/catalog/contributors) and [Other Datasets]({{site.baseurl}}/catalog/other_datasets) pages, along with some datasets not available in Hugging Face.
> * Of the 77,000, 17,000 "attempt" to define licenses, but do so improperly. Licenses are specified as [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, 17,600 datasets specify undefined (i.e., &ldquo;404&rdquo;) URLs. We discarded those datasets, leaving 59,400.<a href="#footnote1"><sup>1</sup></a>
> * The groupings are based on the presence of relevant keywords. Note that _all_ the datasets list their language as `en` (English), but many have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)!).
> * All keywords were converted to lower case before &ldquo;grouping&rdquo;.
> * When a section for a keyword lists _additional keywords_, it means we grouped together different keywords that we believe are related to the same topic, including synonyms. (Please [point out](mailto:data@thealliance.ai) any errors!) In these cases, we also show a **Keyword** column in the corresponding tables, so you can see which keyword was used to include the dataset. (This also means that occasionally some datasets will be listed more than once in their table.)
> * **Important:** At this time, we are not yet validating datasets to ensure their metadata accurately reflect the data records themselves.
>
> <a name="#footnote1">1</a>: Some of the bad license links clearly intend to reference known licenses. We'll revisit those cases.
>
> Do you know of any datasets that should be shown, but aren't? [Let us know!](mailto:data@thealliance.ai)

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
