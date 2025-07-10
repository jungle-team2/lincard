# utils/opengraph.py
import requests
from bs4 import BeautifulSoup


def fetch_opengraph_data(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        og = {
            "title": soup.find("meta", property="og:title"),
            "image": soup.find("meta", property="og:image"),
            "description": soup.find("meta", property="og:description"),
        }

        return {
            "title": og["title"]["content"] if og["title"] else "",
            "image": og["image"]["content"] if og["image"] else "",
            "description": og["description"]["content"] if og["description"] else "",
        }

    except Exception as e:
        return {
            "title": "",
            "image": "",
            "description": "",
        }
