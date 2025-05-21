---
layout: default
title: European Languages
nav_order: 4000
has_children: false
parent: Language Datasets
grand_parent: Dataset Catalog
---

# European Languages

Ancient and modern languages in Europe.

Some are _pidgins_ or _creoles_ derived from languages originating elsewhere.

> **NOTE:** We have endeavored to place languages in their correct geographic location. Some languages cross geographic boundaries. Please report any errors! Thank you.

{% for member in site.language %}
  {% if member.parent_tag == 'europe' %}
    {{ member.content }}
  {% endif %}
{% endfor %}
