import argparse
import os
import requests
import subprocess
import re
from bs4 import BeautifulSoup

def download_pdf(url, output_dir):
    # Get the filename from the URL
    filename = os.path.basename(url)

    # Download the PDF file
    response = requests.get(url)
    if response.status_code == 200:
        # Save the PDF file to the output directory
        with open(os.path.join(output_dir, filename), 'wb') as f:
            f.write(response.content)
        return os.path.join(output_dir, filename)
    else:
        return None

def convert_pdf_to_html(pdf_path, output_dir):
    # Use pdf2htmlEX to convert the PDF to HTML
    subprocess.run(['pdf2htmlEX', pdf_path, os.path.join(output_dir, 'output.html')])

def extract_text_and_images(html_path):
    # Parse the HTML file with BeautifulSoup
    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract text from the HTML file
    text = soup.get_text()

    # Extract images from the HTML file
    images = []
    for img in soup.find_all('img'):
        if img['src'].startswith('data:image/'):
            # Extract images that are embedded in the HTML file
            images.append(img['src'])
        else:
            # Extract images that are linked to in the HTML file
            image_url = img['src']
            if not image_url.startswith('http'):
                # Make the image URL absolute if it is relative
                image_url = os.path.join(os.path.dirname(html_path), image_url)
            images.append(image_url)

    return text, images

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download a PDF and extract text and images from it')
    parser.add_argument('--url', default='https://arxiv.org/abs/2307.15710',help='The URL of the PDF to download')
    parser.add_argument('--output-dir', '-o', default='./', help='The directory to save the downloaded PDF and generated HTML files')
    args = parser.parse_args()

    # Download the PDF file
    pdf_path = download_pdf(args.url, args.output_dir)
    if pdf_path is None:
        print('Failed to download PDF')
        exit(1)

    # Convert the PDF to HTML
    convert_pdf_to_html(pdf_path, args.output_dir)

    # Extract text and images from the HTML file
    html_path = os.path.join(args.output_dir, 'output.html')
    text, images = extract_text_and_images(html_path)

    # Print the extracted text and images
    print('Extracted text:')
    print(text)
    print('Extracted images:')
    print(images)
