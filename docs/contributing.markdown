---
layout: default
title: Contribute a Dataset
nav_order: 30
has_children: false
show_contribute_dataset_button: false
---

# Contribute a Dataset 

> **NOTE:**
> Be sure to read all the [Dataset Requirements]({{site.baseurl}}/dataset-requirements/dataset-requirements) before proceeding. Make sure you agree to all the provisions or contact us at [data@thealliance.ai](mailto:data@thealliance.ai) if you have questions.

## The Contribution Process

The process follows these steps:

1. **Prepare your contribution:** Prepare the [The Dataset Card]({{site.baseurl}}/dataset-requirements/dataset-card-template).
2. **Complete the contribution form:** The form [below](#contribute-your-dataset) submits your dataset for consideration.
3. **Receive Feedback from Us:** We will evaluate the dataset card and the dataset itself, providing feedback and requesting clarifications where needed.
4. **Upload the Data:** (Optional) Once your contribution is accepted, you can transfer the data to [our datasets catalog](https://huggingface.co/aialliance) or you can continue to host it yourself, for example, in your own Hugging Face account.
5. **Review Your Submission Details:** Verify that your data is correctly categorized and labeled in our [catalog](https://huggingface.co/aialliance).
4. **Monitor Usage:** Track how your data is being used by others.

## Now to Contribute Your Dataset

Use this form to tell us about your dataset. We will follow up with next steps.

<div class="callout-box centered bold">
  <em>Contributions will be open soon!</em>
</div>

<!-- 
<form action="#" method="post" id="dataset-contribution-form">
  <div class="form-dataset disabled" inert> 
-->
<form id="dataset-contribution-form">
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
				  <label for="dataset-url">Dataset&nbsp;location:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="url" id="dataset-url" name="dataset-url" class="form-dataset-table-input" placeholder="https://example.com" pattern="https://.*" required />
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset-alliance-hosting">Hosting:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="checkbox" id="dataset-alliance-hosting" name="dataset-alliance-hosting" checked /> I want the AI Alliance to host this dataset.
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
				  <label for="dataset-card">Dataset&nbsp;card:</label>
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
            <input type="checkbox" id="dataset-modality-image" name="dataset-modality-image" class="form-dataset-table-checkbox" />
            <label for="images">Images</label>
          </div>
          <div>
            <input type="checkbox" id="dataset-modality-audio" name="dataset-modality-audio" class="form-dataset-table-checkbox" />
            <label for="audio">Audio</label>
          </div>
          <div>
            <input type="checkbox" id="dataset-modality-video" name="dataset-modality-video" class="form-dataset-table-checkbox" />
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
				  <label for="dataset-email">Email:</label>
				</th>
				<td class="form-dataset-table-value">
				  <input type="email" id="dataset-email" name="dataset-email" class="form-dataset-table-input" placeholder="Your email address" required />	  
				</td>
			</tr>
			<tr>
				<th class="form-dataset-table-label">
    			&nbsp;
    		</th>
				<td class="form-dataset-table-value">
				  <input type="checkbox" name="dataset-agree-to-terms" id="dataset-agree-to-terms" required /> I agree to the terms for contribution.
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
  /* It's necessary to have the file browser limit all the allowed
   * sections to what "accept=''" specifies. 
   */
  var test = document.querySelector('input');
  const form = document.getElementById('dataset-contribution-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = {
        fields: [
          {
            name: 'dataset-name',
            value: document.getElementById('dataset-name').value
          },
          {
            name: 'dataset-url',
            value: document.getElementById('dataset-url').value
          },
          {
            name: 'datasert-alliance-hosting',
            value: document.getElementById('dataset-alliance-hosting').value
          },
          {
            name: 'dataset-card',
            value: document.getElementById('dataset-card').value
          },
          {
            name: 'dataset-modality-text',
            value: document.getElementById('dataset-modality-text').value
          },
          {
            name: 'dataset-modality-image',
            value: document.getElementById('dataset-modality-image').value
          },
          {
            name: 'dataset-modality-audio',
            value: document.getElementById('dataset-modality-audio').value
          },
          {
            name: 'dataset-modality-video',
            value: document.getElementById('dataset-modality-video').value
          },
          {
            name: 'dataset-domain',
            value: document.getElementById('dataset-domain').value
          },
          {
            name: 'dataset-other-domain',
            value: document.getElementById('dataset-other-domain').value
          },
          {
            name: 'dataset-email',
            value: document.getElementById('dataset-email').value
          },
          {
            name: 'dataset-agree-to-terms',
            value: document.getElementById('dataset-agree-to-terms'),value
          }
        ],
        context: {
          hutk: document.cookie.match(/hubspotutk=(.*?);/)[1] || ""  // HubSpot tracking cookie (optional)
        }
      };
      console("form: "+JSON.stringify(formData));
      try {
        /* https://api.hsforms.com/submissions/v3/integration/submit/:portalId/:formGuid' */
        const response = await fetch('localhost:8080/anything', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });

        if (response.ok) {
          alert('Form successfully submitted!', response);
        } else {
          alert('Form submission failed', response);
          console.error('Form submission failed', response);
        }
      } catch (error) {
        alert('Other Error:', error);
        console.error('Other Error:', error);
      }
  });
</script>
