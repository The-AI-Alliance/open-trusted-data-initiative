from data_processing.data_access import DataAccessFactory
from hf_dataset_explorer.python import DatasetExplorerTransform


# create parameters
input_data_factory = DataAccessFactory()
input_data_factory.apply_input_params(
    args={"data_hf_config": {"input_folder": "datasets/"}}
)
output_data_factory = DataAccessFactory()
dataset_explorer_params = {
    "data_access_factory": [input_data_factory, output_data_factory]
}

if __name__ == "__main__":
    # Here we show how to run outside of the runtime
    # Create and configure the transform.
    transform = DatasetExplorerTransform(dataset_explorer_params)
    # get data
    data_access = input_data_factory.create_data_access()
    f_name = "datasets/blublinsky/test/README.md"
    data, _ = data_access.get_file(f_name)
    # Transform the file
    files_list, metadata = transform.transform_binary(file_name=f_name, byte_array=data)
    print(f"\noutput files: {files_list}")
    print(f"output metadata : {metadata}")