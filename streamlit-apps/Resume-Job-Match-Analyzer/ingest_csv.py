import pandas as pd
from database import JobDatabase
from embeddings import EmbeddingManager
import uuid
from tqdm import tqdm

import re

def ingest_csv(file_path, batch_size=100):
    db = JobDatabase()
    embedding_manager = EmbeddingManager()
    
    print("Resetting collection...")
    db.reset_collection()
    
    print(f"Starting ingestion from {file_path}...")
    
    # Define AI/ML/DL keywords for filtering with regex for whole words
    keywords = [
        r'\bai\b', r'artificial intelligence', r'machine learning', r'deep learning', 
        r'data scientist', r'data science', r'\bnlp\b', r'natural language processing',
        r'computer vision', r'neural network', r'reinforcement learning', r'ml engineer',
        r'generative ai', r'\bllm\b', r'large language model'
    ]
    pattern = re.compile('|'.join(keywords), re.IGNORECASE)
    
    # Read CSV in chunks
    chunks = pd.read_csv(file_path, chunksize=batch_size)
    
    total_processed = 0
    total_ingested = 0
    for chunk in chunks:
        ids = []
        titles = []
        companies = []
        descriptions = []
        
        # Prepare data for batch with filtering
        for _, row in chunk.iterrows():
            title = str(row['job_title'])
            desc = str(row['descriptions'])
            
            # Check if any keyword matches as a whole word
            if pattern.search(title) or pattern.search(desc):
                ids.append(str(row['job_id']))
                titles.append(str(row['job_title']))
                companies.append(str(row['company']))
                descriptions.append(str(row['descriptions']))
            
        if ids:
            # Generate embeddings for the filtered batch
            embeddings = embedding_manager.get_embeddings(descriptions)
            
            # Add to database
            db.add_job_postings_batch(ids, titles, companies, descriptions, embeddings)
            total_ingested += len(ids)
        
        total_processed += len(chunk)
        if total_processed % 1000 == 0:
            print(f"Processed {total_processed} jobs, ingested {total_ingested} matching roles...")

    print(f"Ingestion complete. Total matching jobs ingested: {total_ingested}")

if __name__ == "__main__":
    ingest_csv("jobstreet_all_job_dataset.csv")
