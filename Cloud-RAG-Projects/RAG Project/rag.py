import os
import requests  
from azure.storage.blob import BlobServiceClient, BlobClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Azure Blob Storage credentials
account_name = "X"
account_key = "X"
container_name = "X"

# Initialize SparkSession (Make sure Spark is correctly set up)
# spark = SparkSession.builder \
#     .appName("AzureBlobProcessing") \
#     .config("spark.jars.packages", "com.microsoft.azure:azure-storage:8.6.5") \
#     .getOrCreate()

# spark.conf.set("spark.hadoop.fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
# spark.conf.set("spark.hadoop.fs.azure.account.key.ragdata123.blob.core.windows.net", account_key )

spark = SparkSession.builder \
    .appName("BlobPDFProcessing") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-azure:3.2.0") \
    .config("fs.azure.account.key.ragdata123.blob.core.windows.net", account_key) \
    .getOrCreate()




# Initialize BlobServiceClient
blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)

# URL of the document to be uploaded
url = "https://github.com/Azure-Samples/azure-openai-rag-workshop/raw/main/data/support.pdf"
response = requests.get(url)

# Ensure the request was successful
if response.status_code == 200:
    # Extract the filename from the URL
    filename = url.split('/')[-1]
    
    # Get a BlobClient to upload the file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    # Upload the file directly from the response content
    blob_client.upload_blob(response.content, overwrite=True)
    print(f"File '{filename}' uploaded successfully to blob storage.")
else:
    print(f"Failed to download the file from {url}. Status code: {response.status_code}")

blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
pdf_data = blob_client.download_blob().readall()


print(pdf_data)