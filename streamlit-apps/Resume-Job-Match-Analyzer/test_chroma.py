import chromadb
import os

try:
    client = chromadb.PersistentClient(path="./test_db")
    print("PersistentClient initialized successfully.")
    collection = client.get_or_create_collection(name="test")
    print("Collection created successfully.")
except Exception as e:
    print(f"Error: {e}")
