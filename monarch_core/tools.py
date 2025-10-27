#tools.py
import os
import io
import sys
from contextlib import redirect_stdout
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

def run_code(code :str)->str:
    """Execute a string of python code and captures its output and errors."""
    print(f"---Running code in interpreter-----\n {code[:200]}....\n---------------")
    output_stream = io.StringIO()
    try:
        with redirect_stdout(output_stream):
            exec(code,{})
        output = output_stream.getvalue()
        if not output:
            return "Excetion Successful: No output produced "
        return f"Execution Successful:\n---\n{output}\n-----"
    except Exception as e:
        return f"Error during execution of code (e)"


AVAILABLE_TOOLS={
    "web_search": web_search,
    "code_interpreter": run_code,
}