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

> **About This Catalog**
>
> The tables in this catalog list the metadata for Hugging Face-hosted datasets that were gathered as follows:
> 
> * The tables reflect a snapshot of the datasets as of June 5<sup>th</sup>, 2025. (Periodic updates are planned.)
> * Of the approximately 350,000 datasets, only those queryable using [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata are considered, about 260,000.
> * Of those, we discard datasets without a specified license, leaving just approximately 60,000!
> * The licenses are specified as corresponding [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, many undefined (&ldquo;404&rdquo;) URLs are specified. We discarded those datasets leaving 45,000.<a href="#footnote1"><sup>1</sup></a>
> * The groupings are based on the presence of relevant keywords. Note that _all_ the datasets list their language as `en` (English), but many have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)).
> * All keywords were converted to lower case before &ldquo;grouping&rdquo;. When a keyword entry lists _additional keywords_, it means we grouped together different keywords that we believe are related to the same topic, including synonyms. In these cases, we also show a **Keyword** column in the corresponding tables, so you can see which keyword was used to include a dataset.
> * **Important:** At this time, we are not yet validating datasets to ensure their metadata accurately reflect the data records themselves.
> * Do you know of any datasets that should be shown, but aren't? [Let us know!](mailto:data@thealliance.ai)
> 
> <a name="#footnote1">1</a>: Some of the bad license links clearly intend to reference known licenses. We'll revisit those cases.

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
