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
> * The tables reflect a snapshot of the datasets as of October 24<sup>th</sup>, 2025. We are updating the snapshot approximately monthly while we work on a more automated, incremental, and iterative process.
> * The _characteristics_ we describe below haven't changed since we started these periodic updates June 5<sup>th</sup>, 2025. However, the numbers gradually increase as more datasets are added to Hugging Face every day. We also round the numbers to the nearest thousands ("Ks").
> * Of the approximately 554K Hugging Face datasets (as of October 24<sup>th</sup>...), 493K of them have queryable [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata. Among the remaining 61K, 33K don't have Croissant metadata (which is actually an improvement over previous snapshots) and 29K _may_ have this metadata, but you are required to request permission to use the dataset first, even to query its metadata!
> * Of the remaining 493K datasets, 370K do **not** specify a license of any kind, so we discard them, leaving just 123K or 25% of those datasets!
> * Of the remaining 123K datasets, 11K "attempt" to define licenses, but do so improperly. Licenses are specified as [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, these 11K datasets specify undefined (i.e., &ldquo;404&rdquo;) URLs. Previously, we discarded those datasets. However, some of the bad license links clearly intend to reference known licenses. We found that the list of licenses supported by [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} is actually quite small, but this is deliberate to encourage people to pick recent versions and to not be overwhelmed by too many choices. However, this also means that many valid licenses can't be properly specified this way. 
> * Instead, we looked at all these cases and found corresponding definitions for most of these additional licenses, with over 1500 of these improperly-specified datasets having _permissive_ licenses (defined below). 
> * After this processing, 109K datasets have identifiable, known licenses, permissive or not.
> * Of these 109K datasets, 95K of them have permissive licenses. **These are the 95K datasets you will find in the catalog.**
>
> How we group the remaining 95K datasets into tables:
>
> * The groupings into tables are based on the corresponding `keywords` associated with the datasets. 
> * The metadata for the datasets all have a `language` field, but **all** values are _either_ `en` (English) or `NULL`, so we ignore this field. 
> * However, many datasets have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)!).
> * All keywords were converted to lower case before grouping.
> * When a table for a keyword lists _additional keywords_ (e.g., [`advertising`]({{.site.baseurl}}/catalog/domain/#advertising)), it means we grouped together different keywords that we believe are related to the same topic, including synonyms. (Please [email us about any errors](mailto:data@thealliance.ai?subject=Errors in the OTDI catalog) or report problems [another way]({{site.baseurl}}/contributing)) In these cases, we also show a **Keyword** column in the corresponding table, so you can see which keyword was used to include the dataset. (This also means that occasionally a dataset will be listed multiple times in its table, once for each keyword.)

## More About the Licenses

More details of our analysis of the licenses can be found in the GitHub repo's [`license-notes.md`](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/main/static-catalog/license-notes.md){:target="repo"}. Here we provide a few more of the interesting details. The [ScanCode LicenseDB](https://scancode-licensedb.aboutcode.org/) project classifies licenses into one of six categories. The 109K &ldquo;good&rdquo; datasets are categorized as follows:

| Category         | Count |
| :--------------- | ----: |
| Permissive       | 92617 |
| Source-available |  6181 |
| Copyleft Limited |  3608 |
| Unstated License |  3262 |
| Public Domain    |  2096 |
| Copyleft         |  1112 |

For our purposes, _Permissive_ and _Public Domain_ qualify as &ldquo;open&rdquo;, yielding 95K datasets. A total of 19 Permissive licenses were found:

|                         License                               | Category         | Count |
| :------------------------------------------------------------ | :--------------- | ----: |
| Apache License 2.0                                            | Permissive       | 48751 |
| MIT License                                                   | Permissive       | 33644 |
| Creative Commons Attribution 4.0 International Public License | Permissive       |  7813 |
| Creative Commons Zero v1.0 Universal                          | Public Domain    |  1755 |
| Open Data Commons Attribution License v1.0                    | Permissive       |   845 |
| Academic Free License v3.0                                    | Permissive       |   775 |
| Creative Commons Attribution 2.0                              | Permissive       |   237 |
| Creative Commons Attribution 3.0                              | Permissive       |   235 |
| The Unlicense                                                 | Public Domain    |   232 |
| Community Data License Agreement Permissive 2.0               | Permissive       |   145 |
| Public Domain Dedication & License                            | Public Domain    |   109 |
| Etalab Open License 2.0 English                               | Permissive       |    40 |
| Educational Community License v2.0                            | Permissive       |    35 |
| Creative Commons Attribution 2.5                              | Permissive       |    30 |
| PostgreSQL License                                            | Permissive       |    19 |
| Microsoft Public License                                      | Permissive       |    19 |
| Community Data License Agreement Permissive 1.0               | Permissive       |    13 |
| zlib License                                                  | Permissive       |     9 |
| ISC License                                                   | Permissive       |     7 |

{: .attention}
> **Important:** At this time, we are not yet validating datasets to ensure their metadata accurately reflect the data records themselves.
>
> **Note:** Some of the datasets filtered out for one of the reasons discussed above are listed separately in our [Contributors]({{site.baseurl}}/catalog/contributors) or [Other Datasets]({{site.baseurl}}/catalog/other_datasets) pages, where we also describe some other useful datasets that are not available in Hugging Face and not yet included in the catalog itself.

{: .tip}
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
