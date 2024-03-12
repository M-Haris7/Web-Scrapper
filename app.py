import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re

# Function to get file extension from content type
def get_file_extension(content_type):
    if 'image/jpeg' in content_type:
        return '.jpg'
    elif 'image/png' in content_type:
        return '.png'
    else:
        return ''

# Specify the URL of the website you want to scrape
url = "https://www.google.com/search?q=Idli&tbm=isch&ved=2ahUKEwjzo66rnOWEAxXo-DgGHVtkAVUQ2-cCegQIABAA&oq=Idli&gs_lp=EgNpbWciBElkbGkyDRAAGIAEGIoFGEMYsQMyChAAGIAEGIoFGEMyCBAAGIAEGLEDMgoQABiABBiKBRhDMgoQABiABBiKBRhDMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIsB1QvwxY3xdwAXgAkAEAmAGjAaABvAWqAQMwLjW4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ6gCCsICCxAAGIAEGLEDGIMBwgIHECMY6gIYJ8ICBBAjGCeIBgE&sclient=img&ei=807rZbNe6PHj4Q_byIWoBQ&bih=730&biw=1536"

# Send an HTTP request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find image tags on the page
    img_tags = soup.find_all('img')

    # Directory to save the images
    save_dir = "food_images"

    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Download and save each image
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url and not img_url.startswith('http'):
            img_url = urllib.parse.urljoin(url, img_url)

        # Sanitize the image name by removing or replacing invalid characters
        img_name = os.path.join(save_dir, re.sub(r'[^a-zA-Z0-9._-]', '_', os.path.basename(img_url)))

        # Get the file extension based on content type
        content_type = requests.head(img_url).headers.get('Content-Type')
        file_extension = get_file_extension(content_type)

        # Append the file extension to the image name
        img_name += file_extension

        urllib.request.urlretrieve(img_url, img_name)
        print(f"Downloaded: {img_name}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
