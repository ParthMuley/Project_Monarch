#tools.py
import os
from serpapi import GoogleSearch

def web_search(query: str):
    """Perform a web search using serpApi and returns the answer."""
    print(f"---Performing web search for {query}---")
    try:
        params={
            "api_key": os.environ["SERPAPI_API_KEY"],
            "engine": "google",
            "q": query,
        }
        search = GoogleSearch(params)
        results=search.get_dict()

        if "answer_box" in results:
            return str(results["answer_box"])
        elif "organic_results" in results and results["organic_results"]:
            return str(results["organic_results"][0].get("snippet", "No snippet found."))
        else:
            return "No definitive results found."
    except Exception as e:
        return f"Error during web search (e)"