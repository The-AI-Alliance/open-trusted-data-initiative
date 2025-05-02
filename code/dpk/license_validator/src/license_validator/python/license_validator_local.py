from data_processing.data_access import DataAccessHF
from data_processing.utils import TransformUtils
from license_validator.python import (
    LicenseValidatorTransform,
    default_license_column,
    license_content_column_key,
)


# create parameters
license_validator_params = {license_content_column_key: default_license_column}

if __name__ == "__main__":
    # Here we show how to run outside of the runtime
    # Create and configure the transform.
    transform = LicenseValidatorTransform(license_validator_params)
    # Use the local data access to read a parquet table.
    data_access = DataAccessHF()
    data, _ = data_access.get_file(
        "datasets/blublinsky/test/data/aai_Latn/train/000_00000.parquet"
    )
    table = TransformUtils.convert_binary_to_arrow(data=data)
    # Transform the table
    table_list, metadata = transform.transform(table)
    print(f"\noutput table: {table_list}")
    print(f"output metadata : {metadata}")
    # try different license column
    transform.license_column = "language"
    table_list, metadata = transform.transform(table)
    print(f"\noutput table: {table_list}")
    print(f"output metadata : {metadata}")