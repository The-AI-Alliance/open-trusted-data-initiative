---
layout: default
title: Contribute Your Dataset!
nav_order: 50
has_children: false
---

# Contribute Your Dataset! 

> **NOTE:**
> Be sure to read the [Dataset Specification]({{site.baseurl}}/dataset-requirements) details before proceeding. If you have questions or concerns about the specification, please [contact us]({{site.baseurl}}/about/#contact-us).

_Contribution_ means adding your dataset to our catalog. You continue to own and host the dataset where you see fit.

## What Kinds of Datasets Do We Want?
We seek a very broad range of datasets, including but not limited to the following.

#### Science and Industry

* `Climate`: Supporting research in climate change, modeling vegetation and water cover, studying agriculture, etc.
* `Marine`: Supporting research on and applications targeted towards marine environments.
* `Materials`: Known chemical and mechanical properties of chemicals useful for research into potential new and improved materials. 
* `Drug Discovery`: Known chemical and medicinal properties of chemicals useful for research into potential new and improved pharmaceuticals. 
* `Semiconductors`: Specific area of materials research focused on improving the state of the art for semiconductor performance and manufacturing.
* `Physics`: Data for physical systems.
* `Software`: Software code bases and supporting datasets, e.g., vulnerability datasets, analyses of software-related failures, etc.

Other science and industrial domains are welcome, too. 

#### Vertical Domains

* `Finance`: Historical market activity and behaviors. Connections to influences like climate, weather events, political events, etc. 
* `Healthcare`: Everything from synthetic patient data for modeling outcomes, to public literature on known diseases and conditions, to diagnostics results and their analysis.
* `Legal`: Jurisdiction-specific data about case law, etc.
specific applications.
* `Social Sciences`: Social dynamics, political activity and sentiments, etc.

Across industries, there are general concerns required for success:

* `Security`: Security vulnerabilities, incidents, etc. for software and other systems, including datasets for red teaming, penetration testing, and other security practices.
* `Safety`: AI safety in all its forms, including suppression of hate speech, assistance with harmful activities, and hallucinations.

#### Modalities

In addition, we welcome datasets with different _modalities_. Hugging Face attempts to determine the modalities of datasets, but you can also use the `tags` to indicate modalities, such as the following:

* `Text`: especially for under-served language.
* `Image`: i.e., still images
* `Audio`: 
* `Video`: optional including audio
* `Time series`: Data for training, tuning, and testing time series models, both general-purpose and for domain-specific applications.

In addition, some industry specific datasets have their own custom formats.

#### Synthetic Datasets

For all of the above categories, synthetic data is important for filling gaps, especially in domains where open datasets are hard to find, such as patient data in healthcare.

## The Contribution Process

The process follows these steps:

1. **Prepare your contribution:** Make sure you meet the [Dataset Specification]({{site.baseurl}}/dataset-requirements) and prepare the dataset card.
2. **Tell us about your dataset:** Follow the instructions in [Contribute Your Dataset](#contribute-your-dataset) below to submit your dataset for consideration.
3. **Receive feedback from us:** After we evaluate the submission, we will provide feedback and request clarifications, where needed.
4. **Be added to our dataset catalog:** Once your contribution is accepted, your dataset will be added to our [catalog]({{site.baseurl}}/catalog).
5. **Review your details:** After publication in our catalog, verify that the information about your dataset is correct.

## License

The Open Trusted Data Initiative is focused on obtaining datasets from submitters who either own them or have a unrestricted, free-to-use license from all owners of data included in the dataset. By contributing a dataset to the catalog, you affirm that with respect to the dataset and all of its data, you are either (1) the owner or (2) you have been granted a license by all owner(s) of the data enabling you to license it to others under an acceptable open license, which gives anyone the right to use, modify, copy, and create derivative works of the data and dataset, among other things. Do not contribute any data that was obtained merely by collecting publicly-visible data from the Internet or from other sources that you do not own or to which you do not have a suitable license.

We prefer the [Community Data License Agreement - Permissive, Version 2.0](https://cdla.dev/permissive-2-0/){:target="cdla"} although [The Creative Commons License, Version 4.0 - CC BY 4.0](https://chooser-beta.creativecommons.org/){:target="cc-by-4"} is also sometimes used.

By contributing the dataset to the Initiative, you grant anyone a license to the dataset and its data under the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/){:target="dco"} (see also our [community contributors page](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md){:target="community"}).  This does not affect your ownership, copyrights and other interests, and rights to and title to the dataset and its data.

## Contribute Your Dataset

Use this form to tell us about your dataset. It will open your email client with the data added and formatted. After we receive your email, we will follow up with next steps.

<div class="callout-box centered bold">
  <em>For questions, send us email at <a href="mailto:data@thealliance.ai?subject=I%20have%20questions%20about%20contributing%20an%20OTDI%20dataset">data@thealliance.ai</a>.</em>
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
                  <input type="url" id="dataset-url" name="dataset-url" class="form-dataset-table-input" placeholder="https://huggingface.co" pattern="https://.*" required />
                </td>
            </tr>
            <tr>
                <th class="form-dataset-table-label">
                  <label for="dataset">Dataset&nbsp;card:</label>
                </th>
                <td class="form-dataset-table-value">
                  <input type="url" id="dataset-card" name="dataset-url" class="form-dataset-table-input" placeholder="https://huggingface.co" pattern="https://.*" /> Leave blank if the location README <em>is</em> the dataset card.
                </td>
            </tr>
            <!--
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
            -->
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
email: ${document.getElementById('email').value}
agree-to-terms: ${document.getElementById('agree-to-terms').value}
            `;
            const body = body1.replace(/ /g, '%20').replace(/:/g, '%3A%20').replace(/\n/g, '%0D%0A');
            const mailto = `mailto:data@thealliance.ai?subject=I%20want%20to%20contribute%20an%20OTDI%20dataset&${body}`
            try {
                window.open(mailto, '_contribute_email').focus();
            } catch (error) {
                console.error('Error formatting or submitting an email:', error);
            }
        });
</script>
