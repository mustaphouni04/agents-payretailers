from googlesearch import search

# Define your search query
query = "latest AI research papers"

# Perform the search and retrieve the top 3 URLs
urls = list(search(query, num_results=3))

print(urls)

import requests
from docling import Document

# Iterate over each URL
for url in urls:
    print(f"Processing URL: {url}")
    try:
        # Fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        html_content = response.text

        # Parse the HTML content using Docling
        document = Document.from_html(html_content)
        text_content = document.get_text()

        # Output the parsed text content
        print("Parsed text content:")
        print(text_content)
        print("-" * 80)

    except Exception as e:
        print(f"Error processing {url}: {e}")
