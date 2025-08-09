---
layout: default
title: African Languages
nav_order: 1000
has_children: false
parent: Language Datasets
grand_parent: Dataset Catalog
---

# African Languages

Ancient and modern languages in Africa.

Some are _pidgins_ or _creoles_ derived from languages originating elsewhere.

{: .note}
> **NOTE:** We have endeavored to place languages in their correct geographic location. Some languages cross geographic boundaries. Please report any errors! Thank you.

<a name="keywords-at-top"></a>

## Keywords for these Languages

<div>
{% for member in site.language %}
  {% if member.parent_tag == "africa" %} 
    <a href="#{{member.cleaned_tag}}" class="topic-btn">{{member.name}}</a>
  {% endif %}
{% endfor %}
</div>

## Datasets for the Keywords

{% for member in site.language %}
  {% if member.parent_tag == "africa" %}
    {{ member.content }}
  {% endif %}
{% endfor %}
