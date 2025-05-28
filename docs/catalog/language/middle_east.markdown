---
layout: default
title: languages in the Middle East
nav_order: 5000
has_children: false
parent: Language Datasets
grand_parent: Dataset Catalog
---

# languages in the Middle East

Ancient and modern languages in the Middle East.

Some are _pidgins_ or _creoles_ derived from languages originating elsewhere.

> **NOTE:** We have endeavored to place languages in their correct geographic location. Some languages cross geographic boundaries. Please report any errors! Thank you.

<a name="keywords-at-top"></a>

## Keywords for these Languages

<div>
{% for member in site.language %}
  {% if member.parent_tag == "middle_east" %} 
    <a href="#{{member.cleaned_tag}}" class="topic-btn">{{member.name}}</a>
  {% endif %}
{% endfor %}
</div>

## Datasets for the Keywords

{% for member in site.language %}
  {% if member.parent_tag == "middle_east" %}
    {{ member.content }}
  {% endif %}
{% endfor %}
