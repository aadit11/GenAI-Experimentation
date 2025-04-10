import os
from langchain_community.utilities import BingSearchAPIWrapper

os.environ["BING_SUBSCRIPTION_KEY"] = ""
os.environ["BING_SEARCH_URL"] = ""

search = BingSearchAPIWrapper(k=1)  # Set k to 1 to retrieve only the top result
results = search.run("give me latest mergers and acquisitions for the last 20 years")

if results:
    top_result = results[0]
    
    # Check if the result is a dictionary with 'title' and 'snippet' keys
    if isinstance(top_result, dict) and 'title' in top_result and 'snippet' in top_result:
        top_result_title = top_result['title']
        top_result_content = top_result['snippet']
        
        # Truncate content to 100 words
        words = top_result_content.split()
        truncated_content = ' '.join(words[:100])
        
        print(f"Title: {top_result_title}")
        print(f"Content (limited to 100 words): {truncated_content}")
    else:
        print("Unexpected format for top result.")
else:
    print("No results found.")
