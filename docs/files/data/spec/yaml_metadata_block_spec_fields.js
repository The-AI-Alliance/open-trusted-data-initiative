const data_for_yaml_metadata_block_spec_fields = 
[
  {
    "field_name": "license", 
    "description": "We <bold>strongly recommend</bold> <code>cdla-permissive-2.0</code> for the <a href=\"https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md#licenses\" target=\"cdla\">Community Data License Agreement – Permissive, Version 2.0</a> and may require it in the future. See the list of permissive licenses we accept in the <a href=\"../catalog/#table-1\">Catalog index page</a>. Use <a href=\"https://huggingface.co/docs/hub/repositories-licenses\" target=\"hf-licenses\">these names</a> for licenses.",
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
    "field_name": "tags", 
    "description": "Useful for indicating target areas for searches, like <code>chemistry</code>, <code>synthetic</code>, etc. See also <code>task_categories</code>. Where applicable, we recommend that you use the categories described below in <a href=\"#diverse-datasets\">Diverse Datasets...</a>.",
    "required": 0
  },
  {
    "field_name": "annotations_creators", 
    "description": "If appropriate. Examples: <code>crowdsourced</code>, <code>found</code>, <code>expert-generated</code>, <code>machine-generated</code> (e.g., using <em>LLMs as judges</em>).",
    "required": 0
  },
  {
    "field_name": "language_creators", 
    "description": "If appropriate. Examples: <code>crowdsourced</code>, <code>found</code>, <code>expert-generated</code>, <code>machine-generated</code> (i.e., synthetic data).",
    "required": 0
  },
  {
    "field_name": "language_details", 
    "description": "One or more of, for example, <code>en-US</code>, <code>fr-FR</code>, etc.",
    "required": 1
  },
  {
    "field_name": "pretty_name", 
    "description": "E.g., <code>Common Chemistry</code>. This is equivalent to the <code>Dataset title/name</code> field in the <a href=\"https://dataandtrustalliance.org/work/data-provenance-standards\" target=\"dta-prov\"}.",
    "required": 1
  },
  {
    "field_name": "size_categories", 
    "description": "E.g., <code>n<1K</code>, <code>100K<n<1M</code>.",
    "required": 0
  },
  {
    "field_name": "source_datasets", 
    "description": "A YAML list; zero or more. Recall our emphasis on <em>provenance</em>. This list is very important, as each source must meet our provenance standards. See also the discussions below.",
    "required": 1
  },
  {
    "field_name": "task_categories", 
    "description": "A YAML list; one or more from the list in <a href=\"https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/pipelines.ts\" target=\"hf-tasks\">this code</a>.",
    "required": 1
  },
  {
    "field_name": "task_ids", 
    "description": "A YAML list; &ldquo;a unique identifier in the format <code>lbpp/{idx}</code>, consistent with HumanEval and MBPP&rdquo; from <a href=\"https://huggingface.co/datasets/CohereForAI/lbpp\" target=\"cohere\">here</a>. See also examples <a href=\"https://huggingface.co/datasets/CohereForAI/lbpp\> target=\"humaneval\">here</a>.",
    "required": 0
  },
  {
    "field_name": "paperswithcode_id", 
    "description": "Dataset id on PapersWithCode (from the URL).",
    "required": 0
  },
  {
    "field_name": "configs", 
    "description": "Can be used to pass additional parameters to the dataset loader, such as <code>data_files</code>, <code>data_dir</code>, and any builder-specific parameters.",
    "required": 0
  },
  {
    "field_name": "config_name", 
    "description": "One or more dataset subsets, if applicable. See the example in <a href=\"https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1\" target=\"hf-datasetcard\"><code>datasetcard.md</code></a> and the discussions <a href=\"https://huggingface.co/docs/hub/en/datasets-manual-configuration\" target=\"hf-manual\">here</a> and <a href=\"https://huggingface.co/docs/datasets/main/en/repository_structure\" target=\"hf-structure\">here</a>.",
    "required": 0
  },
  {
    "field_name": "dataset_info", 
    "description": "Can be used to store the feature types and sizes of the dataset to be used in Python. See the discussion in <a href=\"https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1\" target=\"hf-datasetcard\"><code>datasetcard.md</code></a>. Also covers the OTDI <code>Data format</code> field.",
    "required": 0
  },
  {
    "field_name": "extra_gated_fields", 
    "description": "Used for protected datasets and hence incompatible with the goals of OTDI.",
    "required": -1
  },
  {
    "field_name": "train-eval-index", 
    "description": "Add this if you want to encode a train and evaluation info in a structured way for AutoTrain or Evaluation on the Hub. See the discussion in <a href=\"https://github.com/huggingface/hub-docs/blob/main/datasetcard.md?plain=1\" target=\"hf-datasetcard\"><code>datasetcard.md</code></a>.",
    "required": 0
  }
];