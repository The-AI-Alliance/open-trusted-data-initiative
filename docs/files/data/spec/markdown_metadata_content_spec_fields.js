const data_for_markdown_metadata_content_spec_fields = 
[
  {
    "field_name": "standards_version_used",
    "description": "A schema version. <em>Standard</em> schemas are not currently specified and TBD.",
    "required": 0,
    "source": "OTDI"
  },
  {
    "field_name": "unique_metadata_identifier",
    "description": "A UUID that is globally unique. We recommend using an <a href=\"https://iscc.codes/\" target=\"iscc\">ISCC code</a>. Derived and synthetic datasets must have their own UUIDs. The UUID is very useful for unambiguous lineage tracking, which is why we require it.",
    "required": 1,
    "source": "OTDI"
  },
  {
    "field_name": "dataset_summary",
    "description": "A concise summary of the dataset and its purpose.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "dataset_description",
    "description": "Describe the contents, scope, and purpose of the dataset, which helps users understand what the data represents, how it was collected, and any limitations or recommended uses. However, this field should not include redundant information covered elsewhere.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "curated_by",
    "description": "One or more legal entities responsible for creating the dataset, providing accountability and a point of contact for inquiries. See also <code>dataset_card_authors</code> below.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "signed_by",
    "description": "A legal review process has determined the dataset is free of any license or governance concerns, and is therefore potentially more trustworthy. The entities that performed the review are listed. (This is not yet required, but is under consideration.)",
    "required": 0,
    "source": "OTDI"
  },
  {
    "field_name": "dataset_sources",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#dataset-sources-optional\" target=\"hf-datasetcard-template-sources\">HF template section</a> (from <a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md\" target=\"hf-datasetcard-template\"><code>datasetcard_template.md</code></a>). Complements the information provided above for <code>source_datasets</code>. The <code>Repository</code> URL &ldquo;subfield&rdquo; is required for each source dataset, <em>unless</em> it was provided by <code>source_datasets</code> in <a href=\"#table-1\">Table 1</a>. The <code>Paper</code> and <code>Demo</code> subfields are optional. See also <code>source_data</code> and <code>source_metadata_for_dataset</code> next.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "source_data",
    "description": "This is redundant with <code>source_datasets</code> in the YAML metadata block. <a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#source-data\" target=\"hf-datasetcard-template-source-data\">HF template section</a>. Use the subsections, described next, <code>data_collection_and_processing_section</code> and <code>source_data_producers_section</code> to describe important provenance information. Is the data synthetic or not? Note our specification above that you can only submit datasets where you have the necessary rights (see also <code>consent_documentation_location</code> below).",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "data_collection_and_processing_section",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#source-data\" target=\"hf-datasetcard-template-source-data\">HF template section</a>. Describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "source_data_producers_section",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#source-data\" target=\"hf-datasetcard-template-source-data\">HF template section</a>. This section describes the people or systems who originally created the data. It should also include self-reported demographic or identity information for the source data creators if this information is available.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "source_metadata_for_dataset",
    "description": "Additional content for <code>source_data</code>; if the corresponding metadata for any dataset is not part of that dataset, then it must be explicitly linked here. This information is necessary for lineage tracking, part of our provenance objectives. Marked required, but if all metadata is part of all datasets (e.g., in <code>README.md</code> dataset cards), then this field can be omitted.",
    "required": 1,
    "source": "OTDI"
  },
  {
    "field_name": "consent_documentation_location",
    "description": "&ldquo;Specifies where consent documentation or agreements related to the data can be found, which help enable legal compliance and regulatory use.&rdquo; Required for third-party datasets you are contributing.",
    "required": 1,
    "source": "OTDI"
  },
  {
    "field_name": "data_origin_geography",
    "description": "&ldquo;The geographical location where the data was originally collected, which can be important for compliance with regional laws and understanding the data's context.&rdquo; Required if restrictions apply.",
    "required": 0,
    "source": "OTDI"
  },
  {
    "field_name": "data_processing_geography_inclusion_exclusion",
    "description": "&ldquo;Defines the geographical boundaries within which the data can or cannot be processed, often for legal or regulatory reasons.&rdquo; Required if restrictions apply.",
    "required": 0,
    "source": "OTDI"
  },
  {
    "field_name": "data_storage_geography_inclusion_exclusion",
    "description": "&ldquo;Specifies where the data is stored and any geographical restrictions on storage locations, crucial for compliance with data sovereignty laws.&rdquo; Required if restrictions apply.",
    "required": 0,
    "source": "OTDI"
  },
  {
    "field_name": "uses",
    "description": "See the <a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#uses\" target=\"hf-datasetcard-template-uses\">HF template section</a>. Optional, but useful for describing <code>Direct Use</code> (field name: <code>direct_use</code>) and <code>Out-of-Scope Use</code> (field name: <code>out_of_scope_use</code>) for the dataset. Consider structuring the <code>Direct Use</code> as described in the <code>Supported Tasks and Leaderboards</code> <a href=\"https://github.com/huggingface/datasets/blob/main/templates/README_guide.md#supported-tasks-and-leaderboards\" target=\"hf-dataset-card-readme-guide\">section</a> in the <code>templates/README_guide.md</code>.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "annotations",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#annotations\" target=\"hf-datasetcard-template-annotations\">HF template section</a>. Add any additional information for the <code>annotations_creators</code> above, if any. Subsections are <code>annotation_process_section</code> and <code>who_are_annotators_section</code>.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "annotation_process_section",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#annotations\" target=\"hf-datasetcard-template-annotations\">HF template section</a>. Describes the annotation process such as annotation tools used in the process, the amount of data annotated, annotation guidelines provided to the annotators, inter-annotator statistics, annotation validation, etc.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "who_are_annotators_section",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#annotations\" target=\"hf-datasetcard-template-annotations\">HF template section</a>. Describes the people or systems who created the annotations.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "bias_risks_limitations",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#bias-risks-and-limitations\" target=\"hf-datasetcard-template-bias-risks-and-limitations\">HF template section</a>. While provenance and governance are the top priorities for OTDI, we also want to communicate to potential users what risks they need to understand about our cataloged datasets. Therefore, we require any information you can provide in this section, along with the <code>Recommendations</code> subsection for mitigations, if known.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "personal_and_sensitive_information",
    "description": "State whether the dataset contains data that might be considered personal, sensitive, or private (e.g., data that reveals addresses, uniquely identifiable names or aliases, racial or ethnic origins, sexual orientations, religious beliefs, political opinions, financial or health data, etc.). Consider using one or more  of the values listed below, after this table. If efforts were made to anonymize the data, describe the anonymization process and also fill in <code>use_of_privacy_enhancing_technologies_pets</code>.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "use_of_privacy_enhancing_technologies_pets",
    "description": "&ldquo;Indicates whether techniques were used to protect personally identifiable information (PII) or sensitive personal information (SPI), highlighting the dataset's privacy considerations.&rdquo;",
    "required": 1,
    "source": "OTDI"
  },
  {
    "field_name": "citation",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#citation\" target=\"hf-datasetcard-template-citation\">HF template section</a>. A place to add <code>BibTeX</code> (field name: <code>citation_bibtex</code>) and <code>APA</code> (field name: <code>citation_apa</code>) citations.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "glossary",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#glossary\" target=\"hf-datasetcard-template-glossary\">HF template section</a>. Define useful terms.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "dataset_card_authors",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#dataset-card-authors-optional\" target=\"hf-datasetcard-template-dataset-card-authors\">HF template section</a>. We need to know the authors.",
    "required": 1,
    "source": "HF"
  },
  {
    "field_name": "dataset_card_contact",
    "description": "<a href=\"https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/datasetcard_template.md#dataset-card-contact\" target=\"hf-datasetcard-template-dataset-card-contact\">HF template section</a>. We need to know whom to contact when needed. Okay to leave blank if the authors' contact information is provided.",
    "required": 0,
    "source": "HF"
  },
  {
    "field_name": "dataset_issue_date",
    "description": "When the dataset was compiled or created. (New versions require new dataset cards.) Recommended format: <code>YYYY-mm-dd:THH:MM:SS</code>",
    "required": 1,
    "source": "OTDI"
  },
  {
    "field_name": "date_previously_issued_version_dataset",
    "description": "Timestamp for previous releases, if applicable. Redundant with other traceability tools, so could be omitted.",
    "required": 0,
    "source": "OTDI"
  },
  {
    "field_name": "range_dates_data_generation",
    "description": "The span of time during which the data within the dataset was collected or generated, offering insight into the dataset's timeliness and relevance.",
    "required": 1,
    "source": "OTDI"
  }
];