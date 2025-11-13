---
layout: default
title: How to Contribute to OTDI
nav_order: 50
has_children: false
---

# How to Contribute to OTDI

There are many ways to contribute. In particular, tell us about other datasets we should catalog!

## Tell Us About Other Datasets

Tell us about other datasets using the [form below](#contribute-your-dataset). If the datasets are already hosted at [Hugging Face](https://huggingface.co){:target="huggingface"}, we have already scanned the metadata for them. However, they won't appear in the OTDI catalog unless they meet some minimum requirements. For example, they must have a permissive license.

{: .note}
> **NOTE:** Be sure to read the [Dataset Specification]({{site.baseurl}}/dataset-requirements/) details before proceeding. If you have questions or concerns about the specification, please [contact us]({{site.baseurl}}/about/#contact-us). See also the [Catalog page]({{site.baseurl}}/catalog/), where we discuss commonly-found problems with the metadata, which you should avoid.

If you prefer, you can also send us [email](mailto:data@thealliance.ai?subject=Datasets you should add to the OTDI catalog), post an [issue](https://github.com/The-AI-Alliance/open-trusted-data-initiative/issues){:target="gh-issues"}, or start a [discussion](https://github.com/The-AI-Alliance/open-trusted-data-initiative/discussions){:target="gh-discussions"}.

## What Kinds of Datasets Do We Seek?

Broad, effective use of AI requires datasets covering the breadth of human languages, domains, modalities, and target applications. See the current [list of keywords]({{site.baseurl}}/catalog/#the-current-keywords-cataloged) we have cataloged. 

We have particular interests in these areas:

#### Science and Industry

| Topic            | Description |
| :--------------- | :---------- |
| `Climate`        | Supporting research in climate change, modeling vegetation and water cover, studying agriculture, etc. |
| `Marine`         | Supporting research on and applications targeted towards marine environments. |
| `Materials`      | Known chemical and mechanical properties of chemicals useful for research into potential new and improved materials.  |
| `Drug Discovery` | Known chemical and medicinal properties of chemicals useful for research into potential new and improved pharmaceuticals.  |
| `Semiconductors` | Specific area of materials research focused on improving the state of the art for semiconductor performance and manufacturing. |
| `Physics`        | Data for physical systems. |
| `Software`       | Software code bases and supporting datasets, e.g., vulnerability datasets, analyses of software-related failures, etc. |

Other science and industrial domains are welcome, too. 

#### Vertical Domains

| Topic             | Description |
| :---------------- | :---------- |
| `Finance`         | Historical market activity and behaviors. Connections to influences like climate, weather events, political events, etc.  |
| `Healthcare`      | Everything from synthetic patient data for modeling outcomes, to public literature on known diseases and conditions, to diagnostics results and their analysis. |
| `Legal`           | Jurisdiction-specific data about case law, etc. specific applications. |
| `Social Sciences` | Social dynamics, political activity and sentiments, etc. |

Across industries, there are general concerns required for success:

| Topic      | Description |
| :--------- | :---------- |
| `Security` | Security vulnerabilities, incidents, etc. for software and other systems, including datasets for red teaming, penetration testing, and other security practices. |
| `Safety`   | AI safety in all its forms, including suppression of hate speech, assistance with harmful activities, and hallucinations. |

#### Modalities

In addition, we welcome datasets with different _modalities_. Hugging Face attempts to determine the modalities of datasets, but you can also use the `tags` to indicate modalities, such as the following:

| Topic         | Description |
| :------------ | :---------- |
| `Text`        | Especially for under-served language. |
| `Image`       | I.e., still images |
| `Audio`       |  |
| `Video`       | Optionally including audio |
| `Time Series` | Data for training, tuning, and testing time series models, both general-purpose and for domain-specific applications. |

In addition, some industry specific datasets have their own custom formats.

#### Synthetic Datasets

For all of the above categories, synthetic data is important for filling gaps, especially in domains where open datasets are hard to find, such as patient data in healthcare.

## Are Your Datasets Truly Open?

Think about these aspects of your datasets:

1. **Permissively licensed?** We can't catalog datasets without a license and those which don't specify one of the permissive licenses listed [here]({{site.baseurl}}/catalog/#more-about-the-licenses)
2. **Other requirements are met?** See the [Dataset Specification]({{site.baseurl}}/dataset-requirements) and prepare the dataset card accordingly. Note that we don't yet enforce the requirements shown, except for the license, but we plan to enforce the whole specification, meaning we will filter out datasets that don't meet its requirements.

## Let Us Know About Your Dataset

{: .note}
> **Note:** If your dataset is hosted by Hugging Face and you meet our requirements discussed above, we will pick it up automatically for the catalog. You can skip the following form. **However**, we would love to hear from you anyway and if you host your dataset elsewhere, you will need to tell us about it here.

Use this form to tell us about your dataset and where it is hosted. It will open your email client with the data added and formatted. After we receive your email, we will follow up with next steps.

<div class="callout-box centered">
  <strong>For questions, send us email at <a href="mailto:data@thealliance.ai?subject=I%20have%20questions%20about%20contributing%20an%20OTDI%20dataset">data@thealliance.ai</a>.</strong>
</div>
<form id="datasets-form">
    <!-- <div class="form-dataset disabled" inert> -->
    <div class="form-dataset"> 
        <table class="form-dataset-table">
            <tr>
                <th class="form-dataset-table-label">
                  <label for="dataset-name">Dataset&nbsp;name:</label>
                </th>
                <td class="form-dataset-table-value">
                  <input type="text" id="dataset-name" name="dataset-name" class="form-dataset-table-input" placeholder="A descriptive and unique name" required />   
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                  <label for="dataset-location">Dataset&nbsp;location:</label>
                </th>
                <td class="form-dataset-table-value">
                  <input type="url" id="dataset-url" name="dataset-url" class="form-dataset-table-input" placeholder="https://some-special-place.com" pattern="https://.*" required />
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                  <label for="dataset">Dataset&nbsp;card:</label>
                </th>
                <td class="form-dataset-table-value">
                  <input type="url" id="dataset-card" name="dataset-url" class="form-dataset-table-input" placeholder="https://some-special-place.com" pattern="https://.*" /> Leave blank if the location README <em>is</em> the dataset card.
                </td>
            </tr>
            {% comment %}
            <tr>
                <th class="form-dataset-table-label">
                  <label for="dataset-hosting">Hosting:</label>
                </th>
                <td class="form-dataset-table-value">
                  <input type="checkbox" id="dataset-alliance-hosting" name="dataset-alliance-hosting" unchecked /> I want the AI Alliance to host this dataset.
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                  <label for="modality">Modalities:</label>
                </th>
                <td class="form-dataset-table-value">
                    <div>
                      <input type="checkbox" id="dataset-modality-text" name="dataset-modality-text" class="form-dataset-table-checkbox" checked />
                      <label for="text">Text</label>
                    </div>
                    <div>
                      <input type="checkbox" id="dataset-modality-text" name="dataset-modality-text" class="form-dataset-table-checkbox" />
                      <label for="images">Images</label>
                    </div>
                    <div>
                      <input type="checkbox" id="dataset-modality-text" name="dataset-modality-text" class="form-dataset-table-checkbox" />
                      <label for="audio">Audio</label>
                    </div>
                    <div>
                      <input type="checkbox" id="dataset-modality-text" name="dataset-modality-text" class="form-dataset-table-checkbox" />
                      <label for="video">Video (including audio)</label>
                    </div>
                    <div>
                      <input type="checkbox" id="dataset-modality-text" name="dataset-modality-text" class="form-dataset-table-checkbox" />
                      <label for="video">Other (e.g., science data)</label>
                    </div>
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                    <label for="domain">Domain:</label>
                </th>
                <td class="form-dataset-table-value">
                  <select id="dataset-domain" name="dataset-domain" class="form-dataset-table-input">
                    <optgroup label="General Purpose">
                      <option default>Not domain specific</option>
                    </optgroup>
                    <optgroup label="Science & Industrial">
                      <option>Climate</option>
                      <option>Marine</option>
                      <option>Materials</option>
                      <option>Semiconductors</option>
                      <option>Time Series</option>
                      <option>Other Industrial</option>
                    </optgroup>
                    <optgroup label="Other">
                      <option>Finance</option>
                      <option>Healthcare</option>
                      <option>Legal</option>
                      <option>Social Science</option>
                    </optgroup>
                  </select>
                  Or another domain? 
                  <input type="text" id="dataset-other-domain" name="dataset-other-domain" class="form-dataset-table-input-shorter" placeholder="Your domain suggestion" required />
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                  <label for="email">Email:</label>
                </th>
                <td class="form-dataset-table-value">
                  <input type="email" id="email" name="email" class="form-dataset-table-input" placeholder="Your email address" required />   
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                &nbsp;
                </th>
                <td class="form-dataset-table-value">
                  <input type="checkbox" id="agree-to-terms" name="agree-to-terms" required /> I agree to the terms for contribution.
                </td>
            </tr>
            {% endcomment %}
            <tr>
                <th class="form-dataset-table-label">
                &nbsp;
                </th>
                <td class="form-dataset-table-value">
                  <input type="submit" value="Submit!" />
                </td>
            </tr>
        </table>
    </div>
</form>
<script>
  <!-- Necessary to have the file browser limit all the allowed sections to what "accept=''" specifies: -->
  var test = document.querySelector('input');

  const form = document.getElementById('datasets-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const body1 = `body=dataset-name: ${document.getElementById('dataset-name').value}
dataset-url: ${document.getElementById('dataset-url').value}
dataset-card: ${document.getElementById('dataset-card').value}
            `;
            const body = body1.replace(/ /g, '%20').replace(/:/g, '%3A').replace(/\n/g, '%0D%0A');
            const mailto = `mailto:data@thealliance.ai?subject=I%20want%20to%20contribute%20an%20OTDI%20dataset&${body}`
            try {
                window.open(mailto, '_contribute_email').focus();
            } catch (error) {
                console.error('Error formatting or submitting an email:', error);
            }
        });
</script>

## Other Ways to Contribute to OTDI

There are many ways you can contribute to the _Open Trusted Data Initiative_.

### Report Errors in Our Catalog

See a mistake in our [catalog]({{site.baseurl}}/catalog)? Send us [email](mailto:data@thealliance.ai?subject=Errors in the OTDI catalog), post an [issue](https://github.com/The-AI-Alliance/open-trusted-data-initiative/issues){:target="gh-issues"}, or start a [discussion](https://github.com/The-AI-Alliance/open-trusted-data-initiative/discussions){:target="gh-discussions"}.

### Help Us Implement Our Data Processing Pipelines

We are working on data processing pipelines, e.g., for evaluating how well datasets match their metadata, claims about licenses, etc., which we discuss on the [How We Process Datasets]({{site.baseurl}}/our-processing/) page.

Want to learn more? Send us [email](mailto:data@thealliance.ai?subject=Data processing pipelines in OTDI), check out our [planned work](https://github.com/orgs/The-AI-Alliance/projects/28/views/1?filterQuery=label%3A%22data+pipelines%22){:target="gh-issues"}, or start a [discussion](https://github.com/The-AI-Alliance/open-trusted-data-initiative/discussions){:target="gh-discussions"}.

### Contribute to This Website

We welcome your contributions to this website itself. The sources are in the [`docs` directory](https://github.com/The-AI-Alliance/open-trusted-data-initiative/tree/main/docs){:target="otdi-repo-docs"} of [this GitHub repo](https://github.com/The-AI-Alliance/open-trusted-data-initiative){:target="otdi-repo"}. Please [post issues](https://github.com/The-AI-Alliance/open-trusted-data-initiative/issues){:target="otdi-repo"} or contribute changes as [pull requests](https://github.com/The-AI-Alliance/open-trusted-data-initiative/pulls){:target="otdi-repo"}. Also, notice that every page has _Edit this page on GitHub_ links, making it easy to go straight to the source of a page to make edits and submit a PR! This is the best way to help us fix typos and make single-page edits.

The repo's [GITHUB_PAGES](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/main/GITHUB_PAGES.md){:target="otdi-repo"} file explains more details for testing the documentation website locally and for creating more extensive changes as PRs.

### Join the Initiative Work Group

See also [Join the Open Trusted Data Initiative Work Group!]({{site.baseurl}}/about/#join-the-open-trusted-data-initiative) on the [About Us]({{site.baseurl}}/about/) page.

