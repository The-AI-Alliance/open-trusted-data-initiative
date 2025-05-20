---
layout: default
title: African Languages
nav_order: 1000
has_children: false
parent: Language Datasets
---
<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet"/>
<script type="text/javascript" src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>

# African Languages

Ancient and modern languages in Africa.

Some are _pidgins_ or _creoles_ derived from languages originating elsewhere.

> **NOTE:** We have endeavored to place languages in their correct geographic location. Some languages cross geographic boundaries. Please report any errors! Thank you.

{% for member in site.language %}
  {% if member.tag != "language" %}
    {{member.content}}
  {% else %}
  	{% for topic in member %}
	  {{member.content}}
	{% endfor %}
  {% endif %}
{% endfor %}
