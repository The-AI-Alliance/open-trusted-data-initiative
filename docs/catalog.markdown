---
layout: default
title: Dataset Catalog
nav_order: 20
has_children: false
---

<link href="https://unpkg.com/tabulator-tables@6.3.1/dist/css/tabulator.min.css" rel="stylesheet"/>
<script type="text/javascript" src="https://unpkg.com/tabulator-tables@6.3.1/dist/js/tabulator.min.js"></script>
<script type="text/javascript">
  function toUpper(str) {
    return str
      .toLowerCase()
      .split(' ')
      .map(function(word) {
        return word[0].toUpperCase() + word.substr(1);
      })
      .join(' ');
 }
</script>

<h1 id="the-dataset-catalog">The Dataset Catalog</h1>

<details open="">
  <summary class="text-delta">
    Table of contents
  </summary>
  <ol id="markdown-toc">
    <li><a href="#datasets-by-categories-tags" id="markdown-toc-datasets-by-categories">Dataset by Categories</a>
      <ol>
        <li><a href="#about-these-datasets" id="markdown-toc-about-these-datasets">About These Datasets</a></li>
        {% for group in site.collections %}
        <li>Category: <a href="#{{group.label}}" id="markdown-toc-{{group.label}}">{{group.label | capitalize }}</a></li>
        {% endfor %}
      </ol>
    </li>
    <li><a href="#dataset-sources" id="markdown-toc-dataset-sources">Dataset Sources</a>
      <ol>
        <li><a href="#brightquery" id="markdown-toc-brightquery">BrightQuery</a></li>
        <li><a href="#common-crawl-foundation" id="markdown-toc-common-crawl-foundation">Common Crawl Foundation</a></li>
        <li><a href="#epfl" id="markdown-toc-epfl">EPFL</a></li>
        <li><a href="#meta" id="markdown-toc-meta">Meta</a></li>
        <li><a href="#pleias" id="markdown-toc-pleias">PleIAs</a></li>
        <li><a href="#servicenow" id="markdown-toc-servicenow">ServiceNow</a></li>
        <li><a href="#semikong" id="markdown-toc-semikong">SemiKong</a></li>
      </ol>
    </li>
    <li><a href="#make-your-contributions" id="markdown-toc-make-your-contributions">Make You Contributions!</a></li>
    <li><a href="#other-ways-to-search-for-datasets" id="markdown-toc-other-ways-to-search-for-datasets">Other Ways to Search For Datasets</a>
      <ol>
        <li><a href="#hugging-face-hub-search" id="markdown-toc-hugging-face-hub-search">Hugging Face Hub Search</a></li>
        <li><a href="#google-dataset-search" id="markdown-toc-google-dataset-search">Google Dataset Search</a></li>
      </ol>
    </li>
  </ol>
</details>

<!-- <blockquote>
  <p><strong>NOTES:</strong></p>
  <ol>
    <li>We are working on a richer interactive browsing and search UI to make it easier to find the datasets for your particular needs.</li>
    <li>The current catalog is a provisional list of datasets. We are still implementing full validation of our <a href="/otdiv2/dataset-requirements">trustworthiness criteria</a>.</li>
  </ol>
</blockquote>
 -->
<h2 id="datasets-by-categories-tags">
  <a href="#datasets-by-categories-tags" class="anchor-heading" aria-labelledby="datasets-by-categories-tags"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Datasets by Categories ("Tags")
</h2>

<h3 id="about-these-datasets">
  <a href="#about-these-datasets" class="anchor-heading" aria-labelledby="about-these-datasets"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>About These Datasets
</h3>

<p>The tables below list Hugging Face-hosted datasets that were gathered as follows:</p>

<ol>
  <li>The tables reflect the data as of May 5<sup>th</sup>, 2025.</li>
  <li>Of the 350,000 or so datasets, only those queryable using <a href="https://mlcommons.org/working-groups/data/croissant/" target="croissant">Croissant</a> metadata are considered, about 260,000.</li>
  <li>Of those, we discarded datasets without a specified license, leaving just 60,000!</li>
  <li>The licenses are specified as URLs at <a href="https://choosealicense.com/licenses/" target="cal">https://choosealicense.com/licenses/</a>. Unfortunately, many undefined URLs are specified, so we discarded those datasets leaving 45,000.</li>
  <li>The groupings are based on the presence of relevant keywords. Note that <em>all</em> the datasets list their language as <code>en</code>, English, but many have keywords for other languages. That's the basis for the <a href="#language">Languages</a> tables.</li>
  <li><strong>Important:</strong> At this time, we are not yet validating datasets to ensure their metadata accurately reflect the data records themselves.</li>
  <li>Do you know of any datasets that should be shown, but aren't? <a href="mailto:data@thealliance.ai">Let us know!</a>. See also our </li>
</ol>

<p>Some of the bad license links clearly intend to reference known licenses. We'll revisit those cases.</p>

{% for collection in site.collections %}
{% unless collection.label == "posts" %}  
<h3 id="{{collection.label}}">
  <a href="#{{collection.label}}" class="anchor-heading" aria-labelledby="{{collection.label}}"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>{{ collection.label | capitalize }}
</h3>

<div class="table-wrapper">
{% for member in site[collection.label] %}
  <a href="#{{collection.label}}-{{member.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph text-center">{{member.name}}</a>
{% endfor %}
</div>

{% for member in site[collection.label] %}
<div id="{{collection.label}}-{{member.tag}}">
  <a href="#{{collection.label}}-{{member.tag}}" class="anchor-heading" aria-labelledby="{{collection.label}}-{{member.tag}}"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>
  <a href="#{{collection.label}}-{{member.tag}}" class="btn btn-primary fs-5 mb-4 mb-md-0 mr-2 no-glyph width-100 text-center">{{member.name}}</a>
  <div id="{{collection.label}}-{{member.tag}}-selected-description-div">
    <blockquote id="{{collection.label}}-{{member.tag}}-selected-description">
      <p>Click a row to see the description. See <a href="#about-these-datasets">About These Datasets</a> for important details.</p>
    </blockquote>
  </div>
  <div id="{{collection.label}}-{{member.tag}}-table" class="table-wrapper">
    <script type="text/javascript" src="{{site.baseurl}}/files/data/catalog/{{collection.label}}/hf_{{member.tag}}.js"></script>
    <script type="text/javascript">
      var {{collection.label}}_{{member.tag}}_table = new Tabulator("#{{collection.label}}-{{member.tag}}-table", {
        height:205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
        data:data_for_{{collection.label}}_{{member.tag}}, //assign data to table
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
      {{collection.label}}_{{member.tag}}_table.on("rowClick", function(e, row){ 
        const data = row.getData();
        const desc = data.description.replace(/\\+[nr]/g, "\n").replace(/\\+t/g, "\t");
        const descDiv = document.getElementById("{{collection.label}}-{{member.tag}}-selected-description");
        const message = `<h4>Name: ${data.name}</h4><h4>URL:</h4> <a href="${data.url}" target="hf">${data.url}</a><h4>Description:</h4><p class="description">${desc}</p>`;
        descDiv.innerHTML = message;
      });
    </script>
  </div>
</div>
{% endfor %}
{% endunless %}
{% endfor %}

<!-- 
<h3 id="domain">
  <a href="#domain" class="anchor-heading" aria-labelledby="domain"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Domains
</h3>

<h3 id="modality">
  <a href="#modality" class="anchor-heading" aria-labelledby="modality"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Modalities
</h3>
 -->

<h2 id="dataset-sources">
  <a href="#dataset-sources" class="anchor-heading" aria-labelledby="dataset-sources"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Dataset Sources
</h2>

<p>The following organizations, shown in alphabetical order, maintain open data sets that are part of our catalog.</p>

<blockquote>
  <p><strong>NOTES:</strong> See also the AI Alliance's <a href="https://huggingface.co/aialliance" target="aia-hf">Hugging Face organization</a> and the <a href="https://huggingface.co/collections/aialliance/open-trusted-data-catalog-66d21b3cb66342762fb6108e" target="aia-hf-otdi">Open Trusted Data Initiative catalog</a> there that includes the datasets listed here.</p>
</blockquote>

<h3 id="brightquery">
  <a href="#brightquery" class="anchor-heading" aria-labelledby="brightquery"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>BrightQuery
</h3>

<p><a href="https://brightquery.ai/" target="bq">BrightQuery</a> ("BQ") provides proprietary financial, legal, and employment information on private and public companies derived from regulatory filings and disclosures. BQ proprietary data is used in capital markets for investment decisions, banking and insurance for KYC & credit checks, and enterprises for master data management, sales, and marketing purposes. In addition, BQ provides public information consisting of clean and standardized statistical data from all the major government agencies and NGOs around the world, and is doing so in partnership with the source agencies. BQ public datasets will be published in OTDI spanning all topics: economics, demographics, healthcare, crime, climate, education, sustainability, etc. Much of the data will be tabular (i.e., structured) time series data, as well as unstructured text.</p>

<p><em>More specific information is coming soon.</em></p>

<h3 id="common-crawl-foundation">
  <a href="#common-crawl-foundation" class="anchor-heading" aria-labelledby="common-crawl-foundation"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Common Crawl Foundation
</h3>

<p><a href="https://commoncrawl.org/" target="ccf">Common Crawl Foundation</a> is working on tagged and filtered crawl subsets for English and other languages.</p>

<p><em>More specific information is coming soon.</em></p>

<h3 id="epfl">
  <a href="#epfl" class="anchor-heading" aria-labelledby="epfl"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>EPFL
</h3>

<p>The <a href="https://huggingface.co/epfl-llm" target="epfl-llm">EPFL LLM team</a> has curated a dataset to train their <a href="https://github.com/epfLLM/meditron" target="meditron">Meditron</a> models. An open-access subset of the medical guidelines data is published on <a href="https://huggingface.co/datasets/epfl-llm/guidelines" target="guidelines">Hugging Face</a>.</p>

<p>See the Meditron GitHub repo <a href="https://github.com/epfLLM/meditron?tab=readme-ov-file#medical-training-data" target="meditron-readme">README</a> for more details about the whole dataset used to train Meditron.</p>

<h3 id="meta">
  <a href="#meta" class="anchor-heading" aria-labelledby="meta"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Meta
</h3>

[Data for Good at Meta](https://dataforgood.facebook.com/dfg/){:target="dfg"} empowers partners with privacy-preserving data that strengthens communities and advances social issues. Data for Good is helping organizations respond to crises around the world and supporting research that advances economic opportunity.

There are 220 datasets available. See [Meta's page](https://data.humdata.org/organization/meta){:target="humdata"} at the [Humanitarian Data Exchange](https://data.humdata.org/){:target="humdata"} for the full list of datasets.

<h3 id="pleias">
  <a href="#pleias" class="anchor-heading" aria-labelledby="pleias"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>PleIAs
</h3>

Domain-specific, clean datasets. 

* PleIAs [website](https://pleias.fr){:target="pleias"}
* PleIAs [Hugging Face organization](https://huggingface.co/PleIAs){:target="pleias-hf"}.
* PleIAs [Collections on Hugging Face](https://huggingface.co/collections/PleIAs){:target="pleias-hf-col"}

| Name             | Description     |  URL     | Date Added |
| :--------------- | :-------------- | :------- | :--------- |
| **Common Corpus** | Largest multilingual pretraining data | [Hugging Face](https://huggingface.co/collections/PleIAs/common-corpus-6734e0f67ac3f35e44075f93){:target="common-corpus"} | 2024-11-04 |
| **Toxic Commons** | Tools for de-toxifying public domain data, especially multilingual and historical text data and data with OCR errors | [Hugging Face](https://huggingface.co/collections/PleIAs/toxic-commons-672243e8ce64b6759e79b6dc){:target="toxic-commons"} | 2024-11-04 |
| **Finance Commons** | A large collection of multimodal financial documents in open data | [Hugging Face](https://huggingface.co/collections/PleIAs/finance-commons-66925e1095c7fa6e6828e26c){:target="finance-commons"} | 2024-11-04 |
| **Bad Data Toolbox** | PleIAs collection of models for the data processing of challenging document and data sources | [Hugging Face](https://huggingface.co/collections/PleIAs/bad-data-toolbox-66981c2d0df662459252844e){:target="bad-data-toolbox"} | 2024-11-04 |
| **Open Culture** | A multilingual dataset of public domain books and newspapers | [Hugging Face](https://huggingface.co/collections/PleIAs/openculture-65d46e3ea3980fdcd66a5613){:target="open-culture"} | 2024-11-04 |

<h3 id="servicenow">
  <a href="#servicenow" class="anchor-heading" aria-labelledby="servicenow"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>ServiceNow
</h3>

Multimodal, code, and other datasets. 

* ServiceNow [website](https://www.servicenow.com){:target="servicenow"}
* ServiceNow [Hugging Face organization](https://huggingface.co/ServiceNow){:target="servicenow-hf"}
* BigCode [Hugging Face organization](https://huggingface.co/bigcode){:target="big-code-hf"}

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **BigDocs-Bench** | A dataset for a comprehensive benchmark suite designed to evaluate downstream tasks that transform visual inputs into structured outputs, such as GUI2UserIntent (fine-grained reasoning) and Image2Flow (structured output). We are actively working on releasing additional components of BigDocs-Bench and will update this repository as they become available. | [Hugging Face](https://huggingface.co/datasets/ServiceNow/BigDocs-Bench){:target="bigdocs-bench"} | 2024-12-11 |
| **RepLiCA**   | RepLiQA is an evaluation dataset that contains Context-Question-Answer triplets, where contexts are non-factual but natural-looking documents about made up entities such as people or places that do not exist in reality... | [Hugging Face](https://huggingface.co/datasets/ServiceNow/repliqa){:target="replica"} | 2024-12-11 |
| **The Stack** | Exact deduplicated version of [The Stack](https://www.bigcode-project.org/docs/about/the-stack/){:target="the-stack"} dataset used for the [BigCode project](https://www.bigcode-project.org){:target="big-code"}. | [Hugging Face](https://huggingface.co/datasets/bigcode/the-stack){:target="the-stack-hf"} | 2024-12-11 |
| **The Stack Dedup** | Near deduplicated version of The Stack (recommended for training). | [Hugging Face](https://huggingface.co/datasets/bigcode/the-stack-dedup){:target="the-stack-dedup"} | 2024-12-11 |
| **StarCoder Data** | Pretraining dataset of [StarCoder](https://huggingface.co/blog/starcoder){:target="starcoder"}. | [Hugging Face](https://huggingface.co/datasets/bigcode/starcoderdata){:target="starcoderdata"} | 2024-12-11 |

<h3 id="semikong">
  <a href="#semikong" class="anchor-heading" aria-labelledby="semikong"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>SemiKong
</h3>

The training dataset for the [SemiKong](https://www.semikong.ai/){:target="semikong"} collaboration that trained an open model for the semiconductor industry.

| Name              | Description     |  URL     | Date Added |
| :---------------- | :-------------- | :------- | :--------- |
| **SemiKong** | An open model training dataset for semiconductor technology | [Hugging Face](https://huggingface.co/datasets/pentagoniac/SemiKong_Training_Datset){:target="semikong-dataset"} | 2024-09-01 |

<h2 id="make-your-contributions">
  <a href="#make-your-contributions" class="anchor-heading" aria-labelledby="make-your-contributions"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Make Your Contributions!
</h2>

To expand this catalog, we [welcome contributions]({{site.baseurl}}/contributing).

<!-- To expand this catalog, we not only [welcome contributions]({{site.baseurl}}/contributing), but we plan to seek out qualified datasets leveraging other sources of information about them, such as the [Data Provenance Initiative](https://www.dataprovenance.org/){:target="dp"}, [Hugging Face](https://huggingface.co/datasets){:target="hf-datasets"}, and others (TBD). -->

<h2 id="other-ways-to-search-for-datasets">
  <a href="#other-ways-to-search-for-datasets" class="anchor-heading" aria-labelledby="other-ways-to-search-for-datasets"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Other Ways to Search For Datasets
</h2>

Until our catalog search is fully operational, there are several ways you can search for datasets that match your criteria.

<h3 id="hugging-face-hub-search">
  <a href="#hugging-face-hub-search" class="anchor-heading" aria-labelledby="hugging-face-hub-search"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Hugging Face Hub Search
</h3>

You can do [full-text search](https://huggingface.co/search/full-text?type=dataset){:target="hf-search"} for datasets, models, and organization spaces in the [Hugging Face Hub](https://huggingface.co/){:target="hf-hub"}. Uncheck _models_ and _spaces_ on the left-hand side to limit your search to datasets. 

For example, searching for _apache croissant_ finds datasets licensed with the Apache 2.0 license that support Croissant metadata. However, using _cdla_ (for Common Data License Agreement) instead of _apache_ also finds a dataset named _CDLA_.

<h3 id="google-dataset-search">
  <a href="#google-dataset-search" class="anchor-heading" aria-labelledby="google-dataset-search"><svg viewbox="0 0 16 16" aria-hidden="true"><use xlink:href="#svg-link"></use></svg></a>Google Dataset Search
</h3>

[Google Dataset Search](https://datasetsearch.research.google.com/){:target="google-ds-search"} is a powerful search engine that finds datasets matching specific criteria across a range of repositories, including Hugging Face.

For example, [this query](https://datasetsearch.research.google.com/search?src=0&query=*&docid=L2cvMTFsZjZjY25jbg%3D%3D&filters=WyJbXCJoYXNfY3JvaXNzYW50X2Zvcm1hdFwiXSIsIltcImZpZWxkX29mX3N0dWR5XCIsW1wibmF0dXJhbF9zY2llbmNlc1wiXV0iLCJbXCJpc19hY2Nlc3NpYmxlX2Zvcl9mcmVlXCJdIl0%3D&property=aXNfYWNjZXNzaWJsZV9mb3JfZnJlZQ%3D%3D){:target="google-ds-search-example"} finds datasets with [Croissant metadata](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} that have permissive licenses allowing free and commercial use, and are focused on the natural sciences. 
