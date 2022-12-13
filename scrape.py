# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# Set the base URL to crawl
base_url = "https://www.example.com"

# Initialize the list of URLs to crawl
urls_to_crawl = [base_url]

# Initialize the list of URLs that have been crawled
crawled_urls = []

# Initialize the list of URLs that use adaptive design or separate mobile URLs
adaptive_urls = []

# Set the maximum number of URLs to crawl
max_urls = 100

# Crawl and index the URLs
while len(urls_to_crawl) > 0 and len(crawled_urls) < max_urls:
    # Get the next URL to crawl
    url = urls_to_crawl.pop()

    # Check if the URL has already been crawled
    if url not in crawled_urls:
        # Crawl the URL
        response = requests.get(url)

        # Check if the URL uses adaptive design or separate mobile URLs
        if "X-UA-Compatible" in response.headers or "Vary" in response.headers:
            # Add the URL to the list of adaptive URLs
            adaptive_urls.append(url)

        # Parse the HTML response
        soup = BeautifulSoup(response.text)

        # Add the URL to the list of crawled URLs
        crawled_urls.append(url)

        # Add any new URLs to the list of URLs to crawl
        for a in soup.find_all('a'):
            link = a.get('href')
            if link not in crawled_urls and link not in urls_to_crawl:
                urls_to_crawl.append(link)

# Print the list of adaptive URLs
print(adaptive_urls)

#Documentation: 
#This script begins by importing the necessary libraries and setting the base URL to crawl. It then initializes the lists of URLs to crawl, URLs that have been crawled, and URLs that use adaptive design or separate mobile URLs.

#Next, the script enters a while loop that continues until there are no more URLs to crawl or the maximum number of URLs has been reached. Within this loop, the script crawls the next URL and checks if it uses adaptive design or separate mobile URLs by looking for specific headers in the HTTP response. If the URL uses one of these techniques, it is added to the list of adaptive URLs.

#The script then parses the HTML response to find any new URLs to crawl, adds the current URL to the list of crawled URLs, and continues the loop. Once all of the URLs have been crawled, the script prints the list of adaptive URLs that were found.

#Note that this is just a simple example of how a web-crawling script could be designed to only crawl and index websites that use adaptive design or separate mobile URLs. A more advanced and robust implementation would likely require additional features and functionality.
