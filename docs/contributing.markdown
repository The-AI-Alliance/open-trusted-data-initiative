---
layout: default
title: Contribute Your Dataset!
nav_order: 50
has_children: false
show_contribute_dataset_button: false
---

# Contribute Your Dataset! 

> **NOTE:**
> Be sure to read all the [Dataset Requirements]({{site.baseurl}}/dataset-requirements/dataset-requirements) before proceeding. Make sure you agree to all the provisions or contact us at [data@thealliance.ai](mailto:data@thealliance.ai) if you have questions.

_Contribution_ means adding your dataset to our catalog. You can optionally _donate_ the dataset to the Alliance, where we take ownership of a copy at the time of donation and we host it ourselves. Otherwise, you continue to own and host the dataset.

## The Contribution Process

The process follows these steps:

1. **Prepare your contribution:** Prepare the [The Dataset Card]({{site.baseurl}}/dataset-requirements/dataset-card-template).
2. **Complete the contribution form:** The form [below](#contribute-your-dataset) submits your dataset for consideration.
3. **Receive feedback from us:** We will evaluate the dataset card and the dataset itself, providing feedback and requesting clarifications where needed.
4. **Upload the data:** (Optional) Once your contribution is accepted, you can transfer the data to be hosted in [The AI Alliance Hugging Face space](https://huggingface.co/aialliance){:target="aia-hf"} or you can continue to host it yourself, for example, in your own Hugging Face space.
5. **Review your submission details:** Verify that your data is correctly categorized and labeled in our catalog.
4. **Monitor usage:** Track how your data is being used by others (Coming soon).

## License

The Open Trusted Data Initiative is focused on obtaining datasets from submitters who either own or have a broad license from all owners of data included in the dataset. By contributing a dataset to the Initative, you affirm that with respect to the dataset and all of its data, you are either (1) the owner or (2) you have been granted a license by all owner(s) of the data enabling you to license it to others under the [Community Data License Agreement - Permissive, Version 2.0](https://cdla.dev/permissive-2-0/){:target="cdla"}, which gives anyone the right to use, modify, copy, and create derivative works of the data and dataset, among other things. Do not contribute any data that was obtained merely by collecting publicly-visible data from the Internet or from other sources that you do not own or to which you do not have a CDLA or compatible license.

By contributing the dataset to the Initiative, you grant anyone a license to the dataset and its data under the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/){:target="dco"} (see also our [community contributors page](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md){:target="community"}) and the [Community Data License Agreement - Permissive, Version 2.0](https://cdla.dev/permissive-2-0/){:target="cdla"}.  This does not affect your ownership, copyrights and other interests, and rights to and title to the dataset and its data.

## Now to Contribute Your Dataset

Use this form to tell us about your dataset. We will follow up with next steps.

> **TIP:** See the [dataset requirements]({{site.baseurl}}/dataset-requirements/dataset-requirements/) for details about each of the following fields.

<div class="callout-box centered bold">
  <em>Contributions will be accepted soon!<br/>Contact us at <a href="mailto:data@thealliance.ai?subject=I want to contribute a dataset">data@thealliance.ai</a> for more information.</em>
</div>
<form id="datasets-hubspot-form">
	<div class="form-dataset disabled" inert>
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
				  <input type="checkbox" id="dataset-alliance-hosting" name="dataset-alliance-hosting" checked /> I want the AI Alliance to host this dataset.
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

const form = document.getElementById('datasets-hubspot-form');
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
                        name: 'dataset-domain',
                        value: document.getElementById('dataset-domain').value
                    },
		    {
                        name: 'email',
                        value: document.getElementById('email').value
                    },
		    {
      			name: 'agree-to-terms',
	 		value: document.getElementById('agree-to-terms'),value
    		    }
                ],
                context: {
                    hutk: document.cookie.match(/hubspotutk=(.*?);/)[1] || ""  // HubSpot tracking cookie (optional)
                }
            };

            try {
              /* https://api.hsforms.com/submissions/v3/integration/submit/:portalId/:formGuid' */
                const response = await fetch('localhost', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    alert('Form successfully submitted!');
                } else {
                    console.error('Form submission failed', response);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
</script>

