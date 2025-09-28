#!/usr/bin/env python3
"""
A simple CLI tool to fetch webpage title and meta description.
Author: likefreedom
"""

import argparse
import requests
from bs4 import BeautifulSoup


def fetch_metadata(url: str):
    """Fetch title and meta description from a webpage."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else "No title found"
    description = None

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and "content" in meta_desc.attrs:
        description = meta_desc["content"].strip()

    return {
        "title": title,
        "description": description or "No description found",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch title and meta description of a webpage."
    )
    parser.add_argument("url", help="The URL of the webpage to fetch")

    args = parser.parse_args()
    result = fetch_metadata(args.url)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Title: {result['title']}")
        print(f"Description: {result['description']}")


if __name__ == "__main__":
    main()
