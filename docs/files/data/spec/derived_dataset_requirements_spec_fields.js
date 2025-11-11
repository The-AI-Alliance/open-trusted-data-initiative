const data_for_derived_dataset_requirements_spec_fields = 
[
  {
    "field_name": "license", 
    "description": "Use the &ldquo;most restrictive&rdquo; upstream license in the source datasets or a suitable alternative. For synthetic data, the license must conform to the model's terms of service.",
    "required": 1
  },
  {
    "field_name": "license_name", 
    "description": "e.g, <em>Community Data License Agreement – Permissive, Version 2.0</em>.",
    "required": 1
  },
  {
    "field_name": "license_link", 
    "description": "e.g, <code>LICENSE</code> or <code>LICENSE.md</code> in the same repo or a URL to another location.",
    "required": 1
  },
  {
    "field_name": "license_details", 
    "description": "Not needed if you use a standard license.",
    "required": 0
  },
  {
    "field_name": "source_datasets", 
    "description": "A YAML list; zero or more. Recall our emphasis on <em>provenance</em>. This list is very important, as each source must meet our provenance standards. See also the discussions below.",
    "required": 1
  },
  {
    "field_name": "pretty_name",
    "description": "A modified name is strongly recommended to avoid potential confusion. It might just embed a version string. It can't be empty.",
    "required": 1
  },
  {
    "field_name": "unique_metadata_identifier",
    "description": "Must have a new value!",
    "required": 1
  },
  {
    "field_name": "dataset_issue_date",
    "description": "The date for this new card.",
    "required": 1
  },
  {
    "field_name": "uses",
    "description": "If the new dataset changes the recommended or allowed ways it can or should be used.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "bias_risks_limitations",
    "description": "Have these changed, e.g., because offensive content was removed from upstream datasets?",
    "required": 1,
    "source": "HF"
  },
];