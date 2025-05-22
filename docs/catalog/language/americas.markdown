---
layout: default
title: Languages in the Americas
nav_order: 2000
has_children: false
parent: Language Datasets
grand_parent: Dataset Catalog
---

# Languages in the Americas

Ancient and modern languages in the Americas.

Some are _pidgins_ or _creoles_ derived from languages originating elsewhere.

> **NOTE:** We have endeavored to place languages in their correct geographic location. Some languages cross geographic boundaries. Please report any errors! Thank you.

## Keywords for These Languages

<div class="table-wrapper">
{% for member in site.language %}
  {% if member.parent_tag == "americas" %} 
    <a href="#{{member.cleaned_tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{member.name}}</a>
  {% endif %}
{% endfor %}
</div>

## Datasets for the Keywords

{% for member in site.language %}
  {% if member.parent_tag == "americas" %}
    {{ member.content }}
  {% endif %}
{% endfor %}
