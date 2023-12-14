import requests
from bs4 import BeautifulSoup

def get_arxiv_vanity_content(arxiv_url):
    # Replace the host name to get the Ar5iv URL
    vanity_url = arxiv_url.replace('https://arxiv.org/abs', 'https://ar5iv.labs.arxiv.org/abs')
    print("Requesting:", vanity_url)
    
    # Send a GET request to the Ar5iv URL
    response = requests.get(vanity_url)
    response.raise_for_status()  # Raise an exception if the request failed

    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print the entire soup object
    print("Soup:")
    print(soup.prettify())

    # Extract the text
    text = soup.get_text()

    # Extract the images
    images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

    # Print the images
    print("Images:")
    for image in images:
        print(image)

    # Extract the meta information
    meta = {meta['name']: meta['content'] for meta in soup.find_all('meta') if 'name' in meta.attrs and 'content' in meta.attrs}

    return text, images, meta

# 使用方法
arxiv_url = 'https://arxiv.org/abs/2307.15710'  # Replace with your URL
text, images, meta = get_arxiv_vanity_content(arxiv_url)
print("Text:", text)
print("Meta:", meta)
