#memory.py

import chromadb
#Initialize the ChromaDB client. It will store data locally in a folder
client=chromadb.Client()

#Get or create a "collection" which is like a table in a traditional database.
#This will create a 'project_monarch'memories' folder if it doesn't exists.
collection=client.get_or_create_collection(name='project_monarch_memories')

def memorize(job_id: str, content: str):
    """Saves a completed job's content to the vector database."""
    try:
        collection.add(
            documents=[content],
            metadatas=[{"type":"job_completion"}],
            ids=[str(job_id)]
        )
        print(f"---Memorized job {job_id}---")
    except Exception as e:
        print(f"Error during memorize: {e}")

def recall(query_texts:str,n_results=1)->list:
    """Recalls similar past jobs from the vector database."""
    try:
        results=collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []
    except Exception as e:
        print(f"Error during recall: {e}")
        return []

