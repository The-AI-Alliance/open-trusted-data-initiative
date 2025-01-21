In majority of cases HF dataset  contains the actual data files in one of the following 
formats: 
* CSV 
* JSON
* JSON lines
* text
* images
* audio
* Parquet

For more complex data formats or including data that is not housed by Hugging face in your HF datat 
set you can use [data set scripts](https://huggingface.co/docs/datasets/dataset_script). 

As explained in the HF documentation


>You implement a dataset script to load and share datasets that consist of data files in unsupported formats 
or require more complex data preparation. This is a more advanced way to define a dataset than using YAML metadata 
in the dataset card. A dataset script is a Python file that defines the different configurations and splits of your 
dataset, as well as how to download and process the data.
>
>The script can download data files from any website, or from the same dataset repository.

A dataset loading script should have the same name as a dataset repository or directory. For example, a repository 
named my_dataset should contain my_dataset.py script. 
```
my_dataset/
├── README.md
└── my_dataset.py
```

Refer to script [template](https://github.com/huggingface/datasets/blob/main/templates/new_dataset_script.py)
to start implementing script loading template

Hugging face also provides an example [script](https://huggingface.co/datasets/aps/super_glue/blob/main/super_glue.py)
wrapping BoolQ Dataset from the [Google Research](https://github.com/google-research-datasets/boolean-questions?tab=readme-ov-file)
into HF data set
