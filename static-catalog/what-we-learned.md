# What We Learned Analyzing Hugging Face Datasets.

While creating the catalog snapshot as of June 6th, 2025, we limited ourselves to datasets hosted at [Hugging Face](https://huggingface.co){:target="hf"}. While analyzing these datasets, we discovered the following statistics about them that we believe many people will find interesting. The following information is also summarized at the beginning of the [catalog landing page](https://the-ai-alliance.github.io/open-trusted-data-initiative/catalog/catalog/){:target="cat"}.

Of the 413,225 Hugging Face datasets, 328,838 of them have queryable [Croissant](https://mlcommons.org/working-groups/data/croissant/){:target="croissant"} metadata, an emerging standard for metadata representation. The Hugging Face  query [API for Croissant metadata](https://huggingface.co/docs/dataset-viewer/en/croissant){:target="hf_cr"} was used. For 328,838 of the datasets, the HTTP success code `200` was returned along with the metadata. Among the 84,387 other datasets, either Croissant data isn't available for them or you have to use an authentication process to access those datasets, even to access the metadata:

| HTTP Code |  Count  | `croissant` |
| --------: |  -----: | :---------- |
|       all | 413,225 | ... │
|     `200` | 328,838 | `{"@context":{...}}` │
|     `400` |  66,131 | `{"error":"The croissant format is not available for this dataset."}` │
|     `401` |  18,256 | `{"error":"Access to dataset <name> is restricted. You must have access to it and be authenticated to access it. Please log in."}` │

Hence, 84,387 datasets can't be included in our catalog tables. However, some of them are listed separately in our [Contributors]({{site.baseurl}}/catalog/contributors) and [Other Datasets]({{site.baseurl}}/catalog/other_datasets) pages, along with some datasets not available in Hugging Face.

Of the 328,838 datasets where Croissant metadata was available, we discarded datasets with no license specified, leaving just 77,007!

Licenses are specified as [choosealicense.com/licenses/](https://choosealicense.com/licenses/){:target="cal"} URLs. Unfortunately, 17,610 of the 77,0007 datasets use undefined (&ldquo;404&rdquo;) URLs. We discarded those datasets, leaving 59,397. Some of the bad license links clearly intend to reference known licenses, but the URLs are not valid. We plan to revisit those cases.

## Keywords

* The groupings are based on the presence of relevant keywords. Note that _all_ the datasets list their language as `en` (English), but many have keywords for other languages. Those keywords are the basis for the [Languages]({{site.baseurl}}/catalog/language/language) tables (including the one for [English]({{site.baseurl}}/catalog/language/europe#english)!).
* All keywords were converted to lower case before &ldquo;grouping&rdquo;.
* When a section for a keyword lists _additional keywords_, it means we grouped together different keywords that we believe are related to the same topic, including synonyms. This was a manual process, but we believe it can be automated and hopefully made more reliable using AI tools.

## Does the Distribution of Keywords Follow a Power Law?
