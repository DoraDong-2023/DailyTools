import os
import requests
import tarfile
import shutil
import re
import json
from bs4 import BeautifulSoup

def download_and_extract_arxiv(url, folder):
    # Create the folder if it does not exist
    os.makedirs(folder, exist_ok=True)

    # Download the tar.gz file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception if the request failed
    tar_gz_path = os.path.join(folder, 'source.tar.gz')
    with open(tar_gz_path, 'wb') as f:
        f.write(response.content)

    # Extract the tar.gz file
    with tarfile.open(tar_gz_path, 'r:gz') as tar:
        tar.extractall(path=folder)

    # Delete the tar.gz file
    os.remove(tar_gz_path)

    # Check if main.tex exists
    main_tex_path = os.path.join(folder, 'main.tex')
    if not os.path.exists(main_tex_path):
        print(f"No main.tex found in {folder}")
        return None

    # Read main.tex
    with open(main_tex_path, 'r') as f:
        tex_content = f.read()

    # Extract document structure
    structure = {
        'title': re.findall(r'\\title{(.*?)}', tex_content),
        'subtitle': re.findall(r'\\subtitle{(.*?)}', tex_content),
        'author': re.findall(r'\\author{(.*?)}', tex_content),
        'abstract': re.findall(r'\\begin{abstract}(.*?)\\end{abstract}', tex_content, re.DOTALL),
        'sections': re.findall(r'\\section{(.*?)}', tex_content),
    }

    # Find all includegraphics commands
    figures = re.findall(r'\\includegraphics.*?{(.*?)}', tex_content)

    # Find all captions
    captions = re.findall(r'\\caption{(.*?)}', tex_content)

    # Combine figures and captions into a dictionary
    images = {f'figure_{i+1}': {'figure': figure, 'caption': caption} for i, (figure, caption) in enumerate(zip(figures, captions))}

    # Combine structure and images into a dictionary
    data = {'text': structure, 'images': images}

    return data

# 使用方法
urls = [
    'https://arxiv.org/e-print/2207.04144v1',
    'https://arxiv.org/e-print/2307.15710',
]
data = {}
for url in urls:
    paper_id = url.rsplit('/', 1)[-1]
    folder = f'./data/{paper_id}'
    paper_data = download_and_extract_arxiv(url, folder)
    if paper_data is not None:
        data[paper_id] = paper_data

# Save data as JSON
with open('data.json', 'w') as f:
    json.dump(data, f)

# Delete the source files
for url in urls:
    paper_id = url.rsplit('/', 1)[-1]
    folder = f'./data/{paper_id}'
    shutil.rmtree(folder)
