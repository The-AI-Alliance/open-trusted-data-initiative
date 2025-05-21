---
layout: default
title: Asian Languages
nav_order: 3000
has_children: false
parent: Language Datasets
grand_parent: Dataset Catalog
---

# Asian Languages

Ancient and modern languages in Asia.

Some are _pidgins_ or _creoles_ derived from languages originating elsewhere.

> **NOTE:** We have endeavored to place languages in their correct geographic location. Some languages cross geographic boundaries. Please report any errors! Thank you.

{% for member in site.language %}
  {% if member.parent_tag == 'asian' %}
    {{ member.content }}
  {% endif %}
{% endfor %}
