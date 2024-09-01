---
layout: default
title: Contribute a Dataset
nav_order: 90
show_contribute_dataset_button: false
---

# How to Contribute a Dataset 

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

* Climate
* Finance
* Healthcare
* Industrial
* Legal
* Marine
* Materials
* Multimedia
* Semiconductors
* Social Sciences
* Timeseries


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
				  <label for="name">Name:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="text" id="name" name="name" class="form-dataset-table-input" required />
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="email">Email:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="email" id="email" name="email" class="form-dataset-table-input" required />	  
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset">Dataset&nbsp;name:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="text" id="dataset" name="dataset" class="form-dataset-table-input" required />	  
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset">Dataset&nbsp;card:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="text" id="dataset" name="dataset" class="form-dataset-table-input" required />
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
							<option>Marine</option>
							<option>Materials</option>
							<option>Semiconductors</option>
							<option>Other Industrial</option>
						</optgroup>
					  <optgroup label="Other">
							<option>Climate</option>
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
    			&nbsp;
    		</th>
				<td class="form-dataset-table-value">
				  <input type="checkbox" name="aggree-to-terms" required /> I agree to the terms for contribution.
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
