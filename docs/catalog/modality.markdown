---
layout: default
title: Modality Datasets
nav_order: 300
has_children: false
parent: catalog
---

<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet"/>
<script type="text/javascript" src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>

# Modality Datasets

<div class="table-wrapper">
{% for member in site.modality %}
  <a href="#{{member.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{member.name}}</a>
{% endfor %}
</div>

{% for member in site.modality %}

## {{member.name}}

This set includes the following keywords: 
<ul>
{% assign all_tags = member.all-tags | split: ' ' %}
  <li>{{ all_tags | join: "</li><li>" }}</li>
</ul>

<!-- <a href="#{{member.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph width-100 text-center">{{member.name}}</a> -->
<div id="{{member.tag}}-selected-description-div">
  <blockquote id="{{member.tag}}-selected-description">
    <p>Click a row to see the description. See <a href="{{site.baseurl}}/catalog/catalog/#about-these-datasets">About These Datasets</a> for important details.</p>
  </blockquote>
</div>

<div id="{{member.tag}}-table" class="table-wrapper">
  <script type="text/javascript" src="{{site.baseurl}}/files/data/catalog/modality/hf_{{member.tag}}.js"></script>
  <script type="text/javascript">
    var {{member.tag}}_table = new Tabulator("#{{member.tag}}-table", {
      height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
      data:data_for_{{member.tag}}, //assign data to table
      layout:"fitColumns", //fit columns to width of table (optional)
      columns:[ //Define Table Columns
        {title:"Name", field:"name"},
        {title:"Keyword", field:"keyword"},
        {title:"License", field:"license"},
        {title:"url", field:"url", formatter:"link", formatterParams:{
          labelField:"url",
          target:"_blank",
        }},
        {title:"Creator", field:"creator_name"},
        {title:"Creator URL", field:"creator_url", formatter:"link", formatterParams:{
          labelField:"url",
          target:"_blank",
        }},
        // {title:"Description", field:"description", formatter:"textarea"},
      ],
      // Doesn't appear to work TODO.
      // tooltips: function (cell) {
      //     let data = cell.getRow();
      //     return "Value of " + data.getRow().getData().name;
      //   }
    });
    {{member.tag}}_table.on("rowClick", function(e, row){ 
      const data = row.getData();
      const desc = data.description.replace(/\\+[nr]/g, "\n").replace(/\\+t/g, "\t");
      const descDiv = document.getElementById("{{member.tag}}-selected-description");
      const message = `<strong>Name:</strong> ${data.name}<br/><strong>Keyword:</strong> ${data.keyword}<br/><strong>URL:</strong> <a href="${data.url}" target="hf">${data.url}</a><br/><strong>Description:</strong><p class="description">${desc}</p>`;
      descDiv.innerHTML = message;
    });
  </script>
</div>
{% endfor %}
