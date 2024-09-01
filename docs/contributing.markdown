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
[Community Data License Agreement - Permissive, Version 2.0](https://cdla.dev/permissive-2-0/).

## Contribute Your Dataset in Four Steps

1. **Prepare your contribution:** Complete the contribution form [below](#contribute-your-dataset) to ensure the dataset is ready for contribution and to prepare the required _data card_.
2. **Upload the Data:** (Optional) Use our services to host the data. Or you can host it yourself, for example, in your own Hugging Face account.
3. **Review & Categorize Your Submission:** Check that your data is correctly categorized and labeled in our catalog.
4. **Monitor Usage:** Track how your data is being used and its impact on AI training.

## It's Your Data, but Our Responsibility

* **Data Anonymization:** We prioritize privacy with built-in data anonymization techniques.
* **Secure Storage:** When we store your data, it is stored securely with state-of-the-art encryption.
* **Ethical Use:** Our platform ensures your data is used ethically and responsibly.


## Diverse Data for Diverse AI Models

We are particularly interested in new datasets that can be used to tune models to excel in various domains.

There are our current data categories:

### Science and Industrial

* Climate - Supporting research in climate change, modeling vegetation and water cover, studying agriculture, etc.
* Marine - Supporting research on and applications targeted towards marine environments.
* Materials - Known chemical and mechanical properties of chemicals useful for research into potential new and existing materials. 
* Semiconductors - Specific area of materials research focused on improving the state of the art for semiconductor performance and manufacturing.
* Other Industrial - Other areas not covered above.

### Other Domains

* Finance - Historical market activity and behaviors. Connections to influences like climate, weather events, political events, etc. 
* Healthcare - Everything from synthetic patient data for modeling outcomes, to public literature on known diseases and conditions, to diagnostics results and their analysis.
* Legal - Jurisdiction-specific data about case law, etc.
* Multimedia - Data for training, tuning, and testing multimodal models, e.g., text and image, including specific applications.
* Social Sciences - Social dynamics, political activity and sentiments, etc.
* Timeseries - Data for training, tuning, and testing time series models, including specific applications.

## Join a Global Community of Innovators

Your participation helps you to achieve the following:

* **Collaborate with Experts:** Connect with data scientists, AI researchers, and industry leaders.
* **Participate in OTDI Forums, Discussions:** Engage in discussions, share insights, and collaborate on projects.
* **Events and Webinars:** Attend exclusive events and webinars to stay updated.

# Contribute Your Dataset

<form action="#" method="post">
	<div class="form-dataset">
		<table class="form-dataset-table">
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset">Dataset&nbsp;name:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="text" id="dataset-name" name="dataset-name" class="form-dataset-table-input" placeholder="A descriptive and unique name" required />	  
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset">Dataset&nbsp;location:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="url" id="dataset" name="dataset" class="form-dataset-table-input" placeholder="https://example.com" pattern="https://.*" required />
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  &nbsp;
				</th>
				<td class="form-dataset-table-value">
				  <input type="checkbox" name="agree-to-terms" checked /> I want the AI Alliance to host this dataset.
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset">Dataset&nbsp;card:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="file" id="dataset-card" name="dataset-card" accept=".txt, .md, .markdown" class="form-dataset-table-input" required />
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="domain">Domain:</label>
				</th>
				<td class="form-dataset-table-value">
					<select id="domain" name="domain" class="form-dataset-table-input">
					  <optgroup label="General Purpose">
							<option default>Not domain specific</option>
					  </optgroup>
					  <optgroup label="Science & Industrial">
							<option>Climate</option>
							<option>Marine</option>
							<option>Materials</option>
							<option>Semiconductors</option>
							<option>Other Industrial</option>
						</optgroup>
					  <optgroup label="Other">
							<option>Finance</option>
							<option>Healthcare</option>
							<option>Legal</option>
							<option>Multimedia</option>
							<option>Social Science</option>
							<option>Time Series</option>
					  </optgroup>
					</select>
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
			    <input type="submit" value="Contribute!" />
				</td>
			</tr>
		</table>
  </div>
</form>
<script>
	<!-- Necessary to have the file browser limit all the allowed sections to what "accept=''" specifies. -->
  var test = document.querySelector('input');
</script>

