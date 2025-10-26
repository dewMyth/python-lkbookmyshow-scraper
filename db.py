from pymongo import MongoClient, errors
from datetime import datetime
from logger import logger
import os


def get_db():
    try:
        logger.info('Attempting to connect to MongoDB...')

        client = MongoClient("mongodb+srv://dewmyth:Lso4hb6eYDc1APjB@cluster0.nvij6jq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        db = client["test"]
        collection = db["movies"]

        # Test connection with a simple ping
        client.admin.command("ping")
        logger.info("Successfully connected to MongoDB.")
        return collection

    except errors.ConnectionFailure as e:
        logger.exception(f"MongoDB connection failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected MongoDB error: {e}")
        raise


# Get data by condition
def find():
    collection = get_db()
    try:
        result = list(collection.find({}))
        if result is not None:
            logger.info(f"Found {len(result)} movies.")
            return result
        else:
            return None
    except errors.OperationFailure as e:
        logger.exception(f"MongoDB operation failed: {e}")
        return None



# Data saving function
def save_data(data):
    collection = get_db()  # get a live collection instance
    try:
        if not data:
            logger.warning("No data to save, skipping insert.")
            return

        result = collection.insert_many(data)
        logger.info(f"Inserted {len(result.inserted_ids)} document into MongoDB.")

    except Exception as e:
        logger.exception(f"Failed to save data: {e}")
