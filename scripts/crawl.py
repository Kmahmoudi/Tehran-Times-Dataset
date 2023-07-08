import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import io
import re

def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)  # Set the timeout value as needed
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"An exception occurred for URL: {url}\n{str(e)}")
        return ""
    return ""

def extract_links(url, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
        same_origin_links = []

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                parsed_url = urlparse(absolute_url)
                if parsed_url.scheme == 'http' or parsed_url.scheme == 'https':
                    same_origin_links.append(absolute_url)

        return same_origin_links
    except Exception as e:
        print(f"An exception occurred for URL: {url}\n{str(e)}")
        return ""


def save_links_to_file(links, filename):
    with io.open(filename, 'w', encoding="utf-8") as file:
        for link in links:
            file.write(link + '\n')


def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.get_text() + ' '

    return text.strip()

def save_text_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with io.open(filepath, 'w', encoding="utf-8") as file:
        file.write(text)


from urllib.parse import urlparse
import os

def crawl(url, directory):
    visited_urls = set()
    links_to_crawl = [url]

    # Check if links file exists
    links_file_path = os.path.join(directory, 'links.txt')
    if os.path.exists(links_file_path):
        with open(links_file_path, 'r') as links_file:
            visited_urls.update(link.strip() for link in links_file.readlines())

    while links_to_crawl:
        current_url = links_to_crawl.pop(0)
        print(current_url)
        visited_urls.add(current_url)

        html = fetch_url(current_url)
        if html:
            links = extract_links(current_url, html)
            same_origin_links = [link for link in links if urlparse(link).netloc == urlparse(url).netloc]
            save_links_to_file(same_origin_links, links_file_path)

            text = extract_text(html)
            filename = urlparse(current_url).path.replace('/', '_') + '.txt'
            save_text_to_file(text, directory, filename)

            for link in same_origin_links:
                if link not in visited_urls and 'news' in link and link not in links_to_crawl:
                    links_to_crawl.append(link)


if __name__ == '__main__':
    start_url = 'https://www.tehrantimes.com/'  # Replace with your desired starting URL
    save_directory = './data'  # Replace with your desired save directory
    crawl(start_url, save_directory)