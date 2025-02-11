# README for `tools-notes`

This folder is not part of the website or production code. It is used to collect "background" notes on various tools, such as dataset tools from Hugging Face. See the enclosed folders for more details.

Some tools are covered with dedicated folders, e.g., those where sample Python scripts are provided. Others are described here.

## Presidio

[Presidio](https://github.com/microsoft/presidio) from Microsoft provides context aware, pluggable, and customizable data protection and de-identification SDK for text and images. 

It is used as part of the processing pipeline for the [PubMed Guidelines](https://huggingface.co/datasets/epfl-llm/guidelines) dataset from the [EPFL LLM team](https://huggingface.co/epfl-llm). This dataset is used to train their [Meditron](https://github.com/epfLLM/meditron) models, which were trained using [their fork](https://github.com/epfLLM/Megatron-LLM) of NVIDIA's [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) training library.