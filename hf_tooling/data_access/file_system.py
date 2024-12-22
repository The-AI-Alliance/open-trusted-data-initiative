from huggingface_hub import HfFileSystem
import pyarrow as pa
import pyarrow.parquet as pq


# create fs. You can specify a token here for authentication
fs = HfFileSystem()

# List all files
files = fs.ls(path="datasets/HuggingFaceFW/fineweb-2/data")
print(f"found {len(files)} files")

# List parquet files
files = fs.glob(path="datasets/HuggingFaceFW/fineweb-2/data/**/*.parquet")
print(f"found {len(files)} files")

# read file
with fs.open(path=files[0], mode="rb") as f:
    data = f.read()
reader = pa.BufferReader(data)
table = pq.read_table(reader)

print(f"got the table with columns {table.column_names}, number of rows {table.num_rows}")

# find path content
files = fs.find(path="datasets/HuggingFaceFW/fineweb-2/data/aai_Latn")
print(files)

# folder info
info = fs.info(path="datasets/HuggingFaceFW/fineweb-2/data/aai_Latn")
print(f"dirctory info {info}")

# walking directory
iterator = fs.walk(path="datasets/HuggingFaceFW/fineweb-2/data/aai_Latn")
for data in iterator:
    print(f"directory {data[0]}, children {data[1]}, files {data[2]}")