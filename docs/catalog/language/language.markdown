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
  {% endif %}
{% endfor %}
</div>

## Datasets for the Language Keywords

<div>
<p>
{% assign current_region = "" %}
{% for member in site.language %}
  {% if member.tag != "language" %} 
    {% comment %} Skip the "index" markdown file {% endcomment %}
    {% assign region = member.parent_tag %}
    {% if region != current_region %}
      {% assign current_region = region %}
  </p>
  <h3><a href="{{site.baseurl}}/catalog/language/{{member.parent_tag}}/">{{member.parent_title}}</a></h3>
  <p>
    {% endif %}
    <a href="{{site.baseurl}}/catalog/language/{{member.parent_tag}}/#{{member.cleaned_tag}}" class="topic-btn">{{member.name}}</a>
  {% endif %}
{% endfor %}
</p>
</div>

