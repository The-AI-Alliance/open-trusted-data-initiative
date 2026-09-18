# What We Learned Analyzing Hugging Face Datasets.

While creating an early snapshot (June 6th, 2025) of the [Open Trusted DAta Initiative](https://the-ai-alliance.github.io/open-trusted-data-initiative/){:target="otdi"} catalog of open datasets, we limited ourselves to datasets hosted by [Hugging Face](https://huggingface.co){:target="hf"}. While analyzing these datasets, we discovered the following limitations about many of them that we believe many people will find interesting. The following information is also summarized at the beginning of the [catalog landing page](https://the-ai-alliance.github.io/open-trusted-data-initiative/catalog/catalog/){:target="cat"}. Note that the list of datasets continues to grow. The numbers shown are for the June 6th snapshot. All would be bigger today.

> **Highlights**
> ...

Of the 413,225 Hugging Face datasets, 328,838 of them have queryable [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata, an emerging standard for metadata representation. The Hugging Face [query API for Croissant metadata](https://huggingface.co/docs/dataset-viewer/en/croissant){:target="hf_cr"} was used. So, for 328,838 of the 413,225 datasets, the HTTP success code `200` was returned along with the metadata. Among the 84,387 other datasets, either Croissant data isn't available for them or you have to use an authentication process to access those datasets, even to access the metadata:

| HTTP Code |  Count  | `croissant` |
| --------: |  -----: | :---------- |
|       all | 413,225 | ... |
|     `200` | 328,838 | `{"@context":{...}}` |
|     `400` |  66,131 | `{"error":"The croissant format is not available for this dataset."}` |
|     `401` |  18,256 | `{"error":"Access to dataset <name> is restricted. You must have access to it and be authenticated to access it. Please log in."}` |

> **Blocker #1:** Datasets where an authentication process is required before seeing the metadata.

Hence, 84,387 datasets can't be included in our catalog tables. However, some of them are listed separately in our [Contributors]({{site.baseurl}}/catalog/contributors) and [Other Datasets]({{site.baseurl}}/catalog/other_datasets) pages, along with some datasets not available in Hugging Face.

Of the 328,838 datasets where Croissant metadata was available, we discarded datasets with no license specified, leaving just 77,007!

> **Blocker #2:** Less than a quarter (23%) of the datasets even bother to specify a license of any kind.

Licenses are specified as [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, 17,610 of the 77,0007 datasets use undefined (&ldquo;404&rdquo;) URLs. We discarded those datasets, leaving 59,397. Some of the bad license links clearly intend to reference known licenses, but the URLs are not valid. In many cases, the license name is also in the keywords. We plan to revisit these records with mis-identified licenses.

> **Blocker #3:** Coincidentally, 23% of the datasets that attempted to specify a license, did not specify a correctly-defined license, although many of these errors could be fixed.

## Keywords

The current catalog tables are based on the keywords specified in the metadata. Hence the keywords are the most important tool we currently use to divide the datasets into topics. In total, we found 22214 unique keywords.

* The groupings are based on the presence of relevant keywords. Note that _all_ the datasets list their `language` as `en` (English), but many have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)!).
* All keywords were converted to lower case before &ldquo;grouping&rdquo;.
* When a section for a keyword lists _additional keywords_, it means we grouped together different keywords that we believe are related to the same topic, including synonyms. This was a manual process, but we believe it can be automated and hopefully made more reliable using AI tools.

> **Blocker #4 (but minor):** Since the `language` field _always_ had the value `en` (English), it's not very useful.

> **Note:** A flaw of relying on the keywords for topic identification is the fact they are provided manually by the dataset owners. There is an opportunity to improve the quality of keywords by identifying the keywords automatically using LLMs. In other words, using classification.

## The Distribution of Keywords

The 59,397 records contain arrays of keywords. We expanded those arrays to have separate records for each keyword, with the other columns duplicated. This resulted in 676,851 records. With this dataset, we analyzed the keywords.

First, here are the top 40 by count:

| keyword              | count |
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


## How Many Keywords Represent Spoken Languages?

We used an [ISO list](https://gist.github.com/jrnk/8eb57b065ea0b098d571) of _codes_ for 184 spoken languages. (Hence, we ignore _programming_ languages.) For example, `en` is the code for English. 

Here are the top 22 languages, where the corresponding code appeared in the number of datasets shown:

| Language      | Count |
| :============ | ====: |
| English       | 14703 |
| Chinese       |  1563 |
| French        |  1095 |
| Russian       |   988 |
| Spanish       |   983 |
| Japanese      |   940 |
| German        |   852 |
| Korean        |   682 |
| Arabic        |   675 |
| Portuguese    |   596 |
| Italian       |   564 |
| Turkish       |   508 |
| Hindi         |   471 |
| Vietnamese    |   423 |
| Catalan       |   235 |
| Hungarian     |   235 |
| Javanese      |   101 |
| Xhosa         |   101 |
| Aragonese     |    30 |
| Nyanja        |    29 |
| Volapük       |    26 |
| Aymara        |    24 |

As expected, English dominates with approximately 10 times the number compated to the next few languages.
