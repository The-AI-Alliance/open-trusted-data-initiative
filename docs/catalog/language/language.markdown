---
layout: default
title: Language Datasets
nav_order: 100
has_children: true
parent: Dataset Catalog
---

# Datasets for Different Languages

<a name="keywords-at-top"></a>

<div>
{% assign current_region = "" %}
{% for member in site.language %}
  {% if member.tag == "language" %} 
    {{ member.content }}
  
    <h2>Language Keywords for the Geographic Regions</h2>

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
