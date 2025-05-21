---
layout: default
title: Language Datasets
nav_order: 100
has_children: true
parent: Dataset Catalog
---

Datasets with different human languages, organized by geographic region in the &ldquo;child&rdquo; pages:

<div class="table-wrapper">
<p>
{% assign current_region = "" %}
{% for member in site.language %}
  {% if member.tag != "language" %} 
    {% comment %} Skip the "index" markdown file {% endcomment %}
    {% assign region = member.parent_tag %}
    {% if region != current_region %}
      {% assign current_region = region %}
  </p>
  <h3>{{member.parent_title}}</h3>
  <p>
    {% endif %}
    <a href="{{site.baseurl}}/catalog/language/{{member.parent_tag}}/#{{member.cleaned_tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{member.name}}</a>
  {% endif %}
{% endfor %}
</p>
</div>

