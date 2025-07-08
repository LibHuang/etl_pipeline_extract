import requests
import json
import boto3
import time
import random
import logging
from io import BytesIO
from datetime import datetime
from typing import Optional

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def upload_api_data_to_s3(
    api_key: str,
    category_id: int,
    bucket_name: str,
    s3_prefix: str,
    limit: int = 48,
    max_retries: int = 3,
    region: Optional[str] = None
) -> None:
    """
    Pulls paginated JSON data from an API and uploads it directly to AWS S3.

    Args:
        api_key (str): RapidAPI key.
        category_id (int): ASOS category ID.
        bucket_name (str): Target S3 bucket.
        s3_prefix (str): S3 folder path prefix.
        limit (int): Number of items per page.
        max_retries (int): Maximum number of retries for failed API calls.
    """
    offset = 0
    categorization = "products"
    base_url = f"https://asos2.p.rapidapi.com/{categorization}/v2/list"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "asos2.p.rapidapi.com"
    }

    s3 = boto3.client("s3", region_name=region) if region else boto3.client("s3")

    while True:
        querystring = {
            "store": "US",
            "offset": str(offset),
            "categoryId": str(category_id),
            "country": "US",
            "sort": "freshness",
            "currency": "USD",
            "sizeSchema": "US",
            "limit": str(limit),
            "lang": "en-US"
        }

        # Retry logic
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(base_url, headers=headers, params=querystring, timeout=10)
                response.raise_for_status()
                data = response.json()
                break
            except requests.exceptions.RequestException as e:
                logging.warning(f"Attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    logging.error("Max retries reached. Aborting.")
                    return
                time.sleep(2 ** attempt)  # Exponential backoff

        # Structured S3 key
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
        filename = f"ASOS_{categorization}_{category_id}_{timestamp}_offset{offset}.json"
        s3_key = f"{s3_prefix}/{filename}"

        # Upload JSON as in-memory stream
        try:
            buffer = BytesIO()
            buffer.write(json.dumps(data, indent=2).encode("utf-8"))
            buffer.seek(0)
            s3.upload_fileobj(buffer, bucket_name, s3_key)
            logging.info(f"Uploaded: s3://{bucket_name}/{s3_key}")
        except Exception as e:
            logging.error(f"Failed to upload {s3_key}: {e}")
            return

        if offset + limit >= data.get("itemCount", 0):
            logging.info("All data retrieved and uploaded.")
            break

        offset += limit
        sleep_time = random.randint(1, 3)
        logging.info(f"Sleeping {sleep_time} seconds before next request")
        time.sleep(sleep_time)
