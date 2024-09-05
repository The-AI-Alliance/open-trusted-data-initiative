---
layout: default
title: Contribute a Dataset
nav_order: 30
has_children: false
show_contribute_dataset_button: false
---

# How to Contribute a Dataset 

By contributing a dataset, you affirm that you are the owner of the dataset
or you have been granted permission by the owner(s) to act on their behalf with respect
to the dataset. You can either retain the current hosting location or have us host it for you.

You retain all ownership, copyrights and other interests, and rights to and title to the
dataset. By contributing the dataset, you grant The AI Alliance a non-exclusive, worldwide, royalty-free, perpetual, and non-cancellable license to use, modify, alter, edit, copy, reproduce, display, make compilations of and distribute the dataset under the
**Community Data License Agreement - Permissive, Version 2.0** [license](https://cdla.dev/permissive-2-0/).

Be sure to read the [Dataset Requirements]({{site.baseurl}}/dataset-requirements/dataset-requirements) before proceeding. 

## Contribute Your Dataset

The process follows these steps:

1. **Prepare your contribution:** Prepare the [The Dataset Card]({{site.baseurl}}/dataset-requirements/dataset-card-template).
2. **Complete the contribution form:** The form [below](#contribute-your-dataset) submits your dataset for consideration.
3. **Receive Feedback from Us:** We will evaluate the dataset card and the dataset itself, providing feedback and requesting clarifications where needed.
4. **Upload the Data:** (Optional) Use our services to host the data. Or you can host it yourself, for example, in your own Hugging Face account.
5. **Review & Categorize Your Submission:** One registered in [our datasets catalog](https://huggingface.co/aialliance), verify that your data is correctly categorized and labeled.
4. **Monitor Usage:** Track how your data is being used and its impact on AI training and other uses.

## It's Your Data, but Our Responsibility

* **Data Anonymization:** We prioritize privacy with built-in data anonymization techniques.
* **Secure Storage:** When we store your data, it is stored securely with state-of-the-art encryption.
* **Ethical Use:** Our platform ensures your data is used ethically and responsibly.


## Diverse Data for Diverse AI Models

We are particularly interested in new datasets that can be used to tune models to excel in various domains, although general-purpose datasets are also welcome. 

When you contribute a dataset, you will have the ability to optionally specify a domain specialty. To keep things relatively simple, we currently only allow one domain specialty to be specified, if any.

These are our current domains:

### Science and Industrial

* **Climate:** Supporting research in climate change, modeling vegetation and water cover, studying agriculture, etc.
* **Marine:** Supporting research on and applications targeted towards marine environments.
* **Materials:** Known chemical and mechanical properties of chemicals useful for research into potential new and existing materials. 
* **Semiconductors:** Specific area of materials research focused on improving the state of the art for semiconductor performance and manufacturing.
* **Other Industrial:** Other areas not covered above.

### Other Domains

* **Finance:** Historical market activity and behaviors. Connections to influences like climate, weather events, political events, etc. 
* **Healthcare:** Everything from synthetic patient data for modeling outcomes, to public literature on known diseases and conditions, to diagnostics results and their analysis.
* **Legal:** Jurisdiction-specific data about case law, etc.
specific applications.
* **Social Sciences:** Social dynamics, political activity and sentiments, etc.
* **Timeseries:** Data for training, tuning, and testing time series models, including specific applications.

In addition, we will ask you clarify the _modality_ of the data. It may contain one or more of the following:

* **Text Only**
* **Images:** (still images)
* **Audio:** 
* **Video:** (including optional audio)


## Join a Global Community of Innovators

Your participation helps you to achieve the following:

* **Collaborate with Experts:** Connect with data scientists, AI researchers, and industry leaders.
* **Participate in OTDI Forums, Discussions:** Engage in discussions, share insights, and collaborate on projects.
* **Events and Webinars:** Attend exclusive events and webinars to stay updated.

# Contribute Your Dataset

Use this form to tell us about your dataset. We will follow up with next steps.

<form action="#" method="post">
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
				  <input type="url" id="dataset-url" name="dataset-url" class="form-dataset-table-input" placeholder="https://example.com" pattern="https://.*" required />
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset-hosting">Hosting:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="checkbox" name="dataset-alliance-hosting" checked /> I want the AI Alliance to host this dataset.
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset">Dataset&nbsp;card:</label>
				</th>
				<td class="form-dataset-table-value">
          <div class="form-dataset-table-file-input">
				    <input type="file" id="dataset-card" name="dataset-card" accept=".txt, .md, .markdown"  required /> (.txt, .md, or .markdown file only)
          </div>
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="modality">Modalities:</label>
				</th>
				<td class="form-dataset-table-value">
          <div>
					  <input type="checkbox" id="dataset-modality-text" name="dataset-modality-text" class="form-dataset-table-checkbox" checked />
            <label for="text">Text Only</label>
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
				  <input type="checkbox" name="agree-to-terms" required /> I agree to the terms for contribution.
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
	<!-- Necessary to have the file browser limit all the allowed sections to what "accept=''" specifies. -->
  var test = document.querySelector('input');
</script>

