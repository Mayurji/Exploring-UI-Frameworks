import chromadb
from chromadb.config import Settings
import os

class JobDatabase:
    def __init__(self, persist_directory="./chroma_db"):
        # Ensure the directory exists
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="job_postings")

    def add_job_posting(self, job_id, title, company, description, extracted_info, embedding):
        """Add a job posting to the collection."""
        self.collection.add(
            ids=[job_id],
            embeddings=[embedding],
            metadatas=[{"title": title, "company": company, "description": description, "extracted_info": extracted_info}],
            documents=[extracted_info]
        )

    def add_job_postings_batch(self, ids, titles, companies, descriptions, embeddings):
        """Add multiple job postings to the collection in a single batch."""
        metadatas = []
        for title, company, desc in zip(titles, companies, descriptions):
            metadatas.append({"title": title, "company": company, "description": desc})
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=descriptions # Using descriptions as documents for batch ingestion
        )

    def query_jobs(self, query_embedding, n_results=5):
        """Query the collection for the best matching jobs."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

    def get_all_jobs(self):
        """Retrieve all job postings."""
        return self.collection.get()

    def delete_job(self, job_id):
        """Delete a job posting by ID."""
        self.collection.delete(ids=[job_id])

    def reset_collection(self):
        """Delete all items in the collection."""
        all_jobs = self.collection.get()
        if all_jobs['ids']:
            self.collection.delete(ids=all_jobs['ids'])
