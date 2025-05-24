---
layout: default
title: Modality Datasets
nav_order: 300
has_children: false
parent: Dataset Catalog
---

# Datasets for Different Modalities

Modalities include `text`, `video`, different widely-applicable problem areas, like data formats, how the data was collected or transformed from other data (e.g., see `text-to-...`), and general topic areas like `pretraining`, `chain of thought`, etc.

<a name="keywords-at-top"></a>

## Keywords for the Modalities

<div class="table-wrapper">
<p>
{% for member in site.modality %}
  {% if member.tag != "modality" %}
    <a href="{{site.baseurl}}/catalog/modality/#{{member.cleaned_tag}}" class="topic-btn">{{member.name}}</a>
  {% endif %}
{% endfor %}
</p>
</div>

## Datasets for the Keywords

{% for member in site.modality %}
  {% if member.tag != "modality" %}
    {{member.content}}
  {% endif %}
{% endfor %}
