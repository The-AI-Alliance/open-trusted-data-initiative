# Used in the pyspark CLI:

from pyspark.sql import SparkSession
from datetime import datetime
import pathlib, sys

spark = SparkSession.builder.appName("ParquetToJSON").getOrCreate()

data_path = "./data/"
parquet_path = f"{data_path}/raw"

df = spark.read.parquet(parquet_path)

print("Schema:")
df.printSchema()
print("Data Preview:")
df.show()

# df.createGlobalTempView('hf')
df.registerTempTable('hf')
df_good = spark.sql("""
	SELECT croissant FROM hf WHERE response_reason = 'OK'
	""")
df_good.count()
df_good.show()
df_good.show(n=1, truncate=False)

df_bad = spark.sql("""
	SELECT croissant FROM hf WHERE response_reason != 'OK'
	""")
df_bad.count()
df_bad.show()
df_bad.show(n=1, truncate=False)

def make_directories(path: str):
	new_dir_path = pathlib.Path(path)
	try:
	    new_dir_path.mkdir(parents=True)
	    print(f"Directory '{new_dir_path}' created successfully.")
	except FileExistsError:
	    print(f"Directory '{new_dir_path}' already exists.")
	except OSError as e:
	    print(f"Error creating directory: {e}")
	    sys.exit(1)

def get_current_datetime_str():
    """Returns the current date and time as a string formatted for file names."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

make_directories(f"{data_path}/json")
json_output_path = f"{data_path}/json/{get_current_datetime_str()}"

df.write.json(json_output_path)

spark.stop()
