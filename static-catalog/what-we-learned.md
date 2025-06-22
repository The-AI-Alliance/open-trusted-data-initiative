# What We Learned Analyzing Hugging Face Datasets.

While creating the catalog snapshot as of June 6th, 2025, we limited ourselves to datasets hosted at [Hugging Face](https://huggingface.co){:target="hf"}. While analyzing these datasets, we discovered the following statistics about them that we believe many people will find interesting. The following information is also summarized at the beginning of the [catalog landing page](https://the-ai-alliance.github.io/open-trusted-data-initiative/catalog/catalog/){:target="cat"}.

Of the 413,225 Hugging Face datasets, 328,838 of them have queryable [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata, an emerging standard for metadata representation. The Hugging Face  query [API for Croissant metadata](https://huggingface.co/docs/dataset-viewer/en/croissant){:target="hf_cr"} was used. For 328,838 of the datasets, the HTTP success code `200` was returned along with the metadata. Among the 84,387 other datasets, either Croissant data isn't available for them or you have to use an authentication process to access those datasets, even to access the metadata:

| HTTP Code |  Count  | `croissant` |
| --------: |  -----: | :---------- |
|       all | 413,225 | ... |
|     `200` | 328,838 | `{"@context":{...}}` |
|     `400` |  66,131 | `{"error":"The croissant format is not available for this dataset."}` |
|     `401` |  18,256 | `{"error":"Access to dataset <name> is restricted. You must have access to it and be authenticated to access it. Please log in."}` |

Hence, 84,387 datasets can't be included in our catalog tables. However, some of them are listed separately in our [Contributors]({{site.baseurl}}/catalog/contributors) and [Other Datasets]({{site.baseurl}}/catalog/other_datasets) pages, along with some datasets not available in Hugging Face.

Of the 328,838 datasets where Croissant metadata was available, we discarded datasets with no license specified, leaving just 77,007!

Licenses are specified as [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, 17,610 of the 77,0007 datasets use undefined (&ldquo;404&rdquo;) URLs. We discarded those datasets, leaving 59,397. Some of the bad license links clearly intend to reference known licenses, but the URLs are not valid. In many cases, the license name is also in the keywords. We plan to revisit these records with mis-identified licenses.

## Keywords

* The groupings are based on the presence of relevant keywords. Note that _all_ the datasets list their language as `en` (English), but many have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)!).
* All keywords were converted to lower case before &ldquo;grouping&rdquo;.
* When a section for a keyword lists _additional keywords_, it means we grouped together different keywords that we believe are related to the same topic, including synonyms. This was a manual process, but we believe it can be automated and hopefully made more reliable using AI tools.

## Does the Distribution of Keywords Follow a Power Law?

The 59,397 records contain arrays of keywords. We expanded those arrays to have separate records for each keyword, with the other columns duplicated. This resulted in 676,851 records. With this dataset, we analyzed the keywords.

First, here are the top 40 by count:

| keyword              | count |
| varchar              | int64 |
| :------------------- | :---- |
| 🇺🇸 region: us        | 59373 |
| croissant            | 52858 |
| datasets             | 52841 |
| polars               | 45056 |
| text                 | 44910 |
| pandas               | 34350 |
| apache-2.0           | 28232 |
| parquet              | 23613 |
| mit                  | 21020 |
| < 1k                 | 17642 |
| 1k - 10k             | 15151 |
| english              | 14882 |
| json                 | 13272 |
| tabular              | 13022 |
| dask                 | 11764 |
| 10k - 100k           | 11134 |
| csv                  |  9263 |
| image                |  7983 |
| robotics             |  6509 |
| video                |  6441 |
| time-series          |  6380 |
| lerobot              |  6378 |
| text-generation      |  6114 |
| 100k - 1m            |  5639 |
| cc-by-4.0            |  5059 |
| question-answering   |  4017 |
| text-classification  |  3502 |
| tutorial             |  3226 |
| crowdsourced         |  2858 |
| imagefolder          |  2797 |
| 1m - 10m             |  2286 |
| so100                |  2128 |
| monolingual          |  2088 |
| cc-by-sa-4.0         |  1929 |
| audio                |  1869 |
| original             |  1585 |
| chinese              |  1431 |
| synthetic            |  1327 |
| summarization        |  1303 |
| text2text-generation |  1213 |
